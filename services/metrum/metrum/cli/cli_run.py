import asyncio
import click
from metrum.common.logger import logger
from metrum.settings import settings
from metrum.collector.metrics import MetricsCollector
from metrum.collector.queries import LogMonitorService
from metrum.sink import create_metric_sink
from datetime import datetime

@click.command()
@click.option('--latest', is_flag=True, help='Only process the latest log file')
def run(latest):
    """Run the Metrum service."""
    logger.info("starting_metrum_service", settings=settings)

    # Initialize services
    metrics_collector = MetricsCollector(db_name="metrum", interval=15)
    log_monitor = LogMonitorService(from_beginning=not latest)
    
    # Initialize metricsink based on settings
    metricsink = create_metric_sink(
        sink_type=settings.metric_sink_type,
        endpoint=settings.metric_sink_endpoint,
        api_key=settings.metric_sink_api_key,
        db_path=settings.metric_sink_db_path,
        pretty=settings.metric_sink_pretty
    )
    
    async def run_services():
        # Start both services concurrently
        await asyncio.gather(
            metrics_collector.start(),
            log_monitor.run()
        )
        
        # Collect and send metrics in a loop
        while True:
            try:
                metrics = await metrics_collector.collect()
                metricsink.write(metrics, datetime.utcnow())
                await asyncio.sleep(metrics_collector.interval)
            except Exception as e:
                logger.error("error_collecting_metrics", error=str(e), exc_info=True)
                await asyncio.sleep(metrics_collector.interval)
    
    try:
        asyncio.run(run_services())
    except KeyboardInterrupt:
        logger.info("service_stopped_by_user")
        # Stop metrics collection and close metricsink on shutdown
        asyncio.run(metrics_collector.stop())
        metricsink.close()
    except Exception as e:
        logger.error("service_error", error=str(e), exc_info=True)
        # Stop metrics collection and close metricsink on error
        asyncio.run(metrics_collector.stop())
        metricsink.close()
        raise 
