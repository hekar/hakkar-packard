import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from metrum.common.logger import logger
from metrum.db.models import LogEvent

import httpx
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


class LogMonitor:
    def __init__(
        self,
        log_file_path: str,
        patterns: Dict[str, Dict[str, str]],
        http_endpoint: str,
        db_url: str,
        poll_interval: float = 1.0,
    ):
        self.log_file_path = Path(log_file_path).absolute()
        self.patterns = patterns
        self.http_endpoint = http_endpoint
        self.engine = create_engine(db_url)
        self.poll_interval = poll_interval
        self.last_position = 0
        self.current_query_buffer = []
        self.current_explain_buffer = []
        self.current_duration = None
        self.current_timestamp = None
        logger.debug("initialized_log_monitor", 
                    log_file=str(self.log_file_path),
                    pattern_count=len(patterns),
                    http_endpoint=http_endpoint,
                    poll_interval=poll_interval)

    def _parse_timestamp(self, line: str) -> Optional[datetime]:
        """Parse timestamp from log line."""
        match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})", line)
        if match:
            timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S.%f")
            logger.debug("parsed_timestamp", timestamp=timestamp.isoformat())
            return timestamp
        logger.debug("failed_to_parse_timestamp", line=line)
        return None

    def _extract_duration(self, line: str) -> Optional[float]:
        """Extract duration from log line."""
        match = re.search(r"duration: ([\d.]+) ms", line)
        if match:
            duration = float(match.group(1))
            logger.debug("extracted_duration", duration_ms=duration)
            return duration
        logger.debug("failed_to_extract_duration", line=line)
        return None

    def _is_query_line(self, line: str) -> bool:
        """Check if line contains a query."""
        is_query = "LOG:  execute" in line
        logger.debug("checked_query_line", is_query=is_query, line=line)
        return is_query

    def _is_explain_line(self, line: str) -> bool:
        """Check if line contains explain plan."""
        is_explain = "LOG:  duration:" in line and "plan:" in line
        logger.debug("checked_explain_line", is_explain=is_explain, line=line)
        return is_explain

    def _is_temporary_file_line(self, line: str) -> bool:
        """Check if line contains temporary file information."""
        is_temp_file = "LOG:  temporary file:" in line
        logger.debug("checked_temp_file_line", is_temp_file=is_temp_file, line=line)
        return is_temp_file

    def _extract_query_text(self, explain_text: str) -> Optional[str]:
        """Extract query text from explain plan."""
        try:
            # Try to parse the JSON in the explain plan
            match = re.search(r'{\s*"Query Text":\s*"([^"]+)"', explain_text)
            if match:
                query_text = match.group(1)
                # Replace escaped newlines
                query_text = query_text.replace('\\n', '\n')
                return query_text
        except Exception as e:
            logger.error("error_extracting_query_text", error=str(e), exc_info=True)
        return None

    def _process_query(self, query_lines: List[str], explain_lines: List[str], duration: Optional[float]) -> Optional[LogEvent]:
        """Process a complete query and its explain plan."""
        if not query_lines:
            return None

        # Extract timestamp from the first line
        timestamp = self._parse_timestamp(query_lines[0])
        if not timestamp:
            return None

        # Extract query text from the explain plan if available
        explain_text = "\n".join(line.split(": ", 1)[1] for line in explain_lines) if explain_lines else None
        query_text = None
        
        if explain_text:
            query_text = self._extract_query_text(explain_text)
        
        # If we couldn't extract from explain plan, try to get from query lines
        if not query_text and query_lines:
            query_text = "\n".join(line.split(": ", 1)[1] for line in query_lines)

        # Match patterns
        pattern_name = None
        for name, pattern_info in self.patterns.items():
            if query_text and re.search(pattern_info["query_pattern"], query_text):
                pattern_name = name
                break

        return LogEvent(
            timestamp=timestamp,
            query_text=query_text,
            explain_text=explain_text,
            duration_ms=duration,
            pattern_name=pattern_name,
        )

    async def _send_event(self, event: LogEvent) -> bool:
        """Send event to HTTP endpoint."""
        async with httpx.AsyncClient() as client:
            try:
                logger.debug("sending_event", 
                           event_id=event.id,
                           pattern_name=event.pattern_name,
                           timestamp=event.timestamp.isoformat())
                response = await client.post(
                    self.http_endpoint,
                    json={
                        "timestamp": event.timestamp.isoformat(),
                        "query_text": event.query_text,
                        "explain_text": event.explain_text,
                        "duration_ms": event.duration_ms,
                        "pattern_name": event.pattern_name,
                    },
                    timeout=10.0,
                )
                success = response.status_code == 200
                logger.debug("event_send_result", 
                           success=success,
                           status_code=response.status_code,
                           event_id=event.id)
                return success
            except Exception as e:
                logger.error("event_send_error", 
                           error=str(e),
                           event_id=event.id,
                           exc_info=True)
                return False

    async def _process_events(self):
        """Process pending events from the database."""
        with Session(self.engine) as session:
            stmt = select(LogEvent).where(LogEvent.status == "pending")
            events = session.execute(stmt).scalars().all()
            logger.debug("processing_pending_events", count=len(events))

            for event in events:
                if await self._send_event(event):
                    event.status = "sent"
                    logger.debug("event_marked_sent", event_id=event.id)
                else:
                    event.status = "failed"
                    logger.debug("event_marked_failed", event_id=event.id)
                session.commit()

    def _read_new_lines(self) -> List[str]:
        """Read new lines from the log file."""
        try:
            with open(self.log_file_path, "r") as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
                logger.debug("read_new_lines", 
                           count=len(new_lines),
                           position=self.last_position)
                return new_lines
        except Exception as e:
            logger.error("error_reading_log_file", 
                        error=str(e),
                        file=str(self.log_file_path),
                        exc_info=True)
            return []

    async def run(self):
        """Main monitoring loop."""
        logger.info("starting_log_monitor", 
                   file=str(self.log_file_path),
                   pattern_count=len(self.patterns))
        
        # Process any existing events on startup
        await self._process_events()

        while True:
            try:
                new_lines = self._read_new_lines()
                
                for line in new_lines:
                    # Extract timestamp from any line that has it
                    timestamp = self._parse_timestamp(line)
                    if timestamp:
                        self.current_timestamp = timestamp
                    
                    if self._is_query_line(line):
                        # Process previous query if exists
                        if self.current_query_buffer:
                            event = self._process_query(
                                self.current_query_buffer,
                                self.current_explain_buffer,
                                self.current_duration
                            )
                            if event:
                                with Session(self.engine) as session:
                                    session.add(event)
                                    session.commit()
                                    logger.debug("saved_new_event", 
                                               event_id=event.id,
                                               pattern_name=event.pattern_name)
                        
                        # Start new query
                        self.current_query_buffer = [line]
                        self.current_explain_buffer = []
                        self.current_duration = None
                        logger.debug("started_new_query_buffer")
                    
                    elif self._is_explain_line(line):
                        self.current_explain_buffer.append(line)
                        self.current_duration = self._extract_duration(line)
                        logger.debug("added_explain_line", 
                                   buffer_size=len(self.current_explain_buffer),
                                   duration=self.current_duration)
                    
                    elif self._is_temporary_file_line(line):
                        # This is the end of an explain plan
                        if self.current_explain_buffer:
                            # Process the complete query with its explain plan
                            event = self._process_query(
                                self.current_query_buffer,
                                self.current_explain_buffer,
                                self.current_duration
                            )
                            if event:
                                with Session(self.engine) as session:
                                    session.add(event)
                                    session.commit()
                                    logger.debug("saved_new_event", 
                                               event_id=event.id,
                                               pattern_name=event.pattern_name)
                            
                            # Reset buffers
                            self.current_query_buffer = []
                            self.current_explain_buffer = []
                            self.current_duration = None
                            logger.debug("processed_explain_plan")
                    
                    elif self.current_query_buffer:
                        self.current_query_buffer.append(line)
                        logger.debug("added_query_line", 
                                   buffer_size=len(self.current_query_buffer))

                # Process any pending events
                await self._process_events()
                
                time.sleep(self.poll_interval)
                
            except Exception as e:
                logger.error("monitor_loop_error", 
                           error=str(e),
                           exc_info=True)
                time.sleep(self.poll_interval) 