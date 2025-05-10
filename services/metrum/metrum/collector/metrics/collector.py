import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import logging
from metrum.collector.metrics.base import BaseMetricsCollector
from metrum.collector.metrics.database import DatabaseMetrics
from metrum.collector.metrics.tables import TableMetrics
from metrum.collector.metrics.indexes import IndexMetrics
from metrum.collector.metrics.functions import FunctionMetrics

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Main metrics collector that orchestrates the collection process."""
    
    def __init__(self, db_name: str, interval: int = 15):
        self.db_name = db_name
        self.interval = interval
        self.collectors: List[BaseMetricsCollector] = [
            DatabaseMetrics(db_name),
            TableMetrics(db_name),
            IndexMetrics(db_name),
            FunctionMetrics(db_name)
        ]
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the metrics collection process."""
        if self._running:
            logger.warning("Metrics collector is already running")
            return
        
        self._running = True
        self._task = asyncio.create_task(self._collect_loop())
        logger.info(f"Started metrics collection for database {self.db_name} with {self.interval}s interval")
    
    async def stop(self):
        """Stop the metrics collection process."""
        if not self._running:
            logger.warning("Metrics collector is not running")
            return
        
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped metrics collection")
    
    async def _collect_loop(self):
        """Main collection loop."""
        while self._running:
            try:
                await self.collect()
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
            
            await asyncio.sleep(self.interval)
    
    async def collect(self) -> Dict[str, List[Dict]]:
        """Collect metrics from all collectors."""
        results = {}
        collection_time = datetime.utcnow()
        
        for collector in self.collectors:
            try:
                collector.last_collection_time = collection_time
                results[collector.table_name] = collector.collect()
                logger.debug(f"Collected metrics from {collector.table_name}")
            except Exception as e:
                logger.error(f"Error collecting metrics from {collector.table_name}: {e}")
        
        return results
    
    def get_column_descriptions(self) -> Dict[str, Dict[str, str]]:
        """Get column descriptions for all collectors."""
        return {
            collector.table_name: collector.get_column_descriptions()
            for collector in self.collectors
        } 