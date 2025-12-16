#!/usr/bin/env python3
"""
#  QuetzalCore Distributed Logging System

# Features:
- Centralized log aggregation
- Real-time log streaming
- Log indexing and search
- Log rotation and archival
- Log analytics
- Alert generation
"""

# import asyncio
# import json
# import gzip
# from datetime import datetime, timedelta
# from typing import List, Dict, Optional, Any
# from dataclasses import dataclass, asdict
# from pathlib import Path
# import logging

# Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


@dataclass
# class LogEntry:
    """A single log entry"""
#     timestamp: str
#     level: str  # DEBUG, INFO, WARNING, ERROR, CRITICAL
#     source: str  # node_id or service name
#     message: str
#     context: Dict[str, Any]
#     trace_id: Optional[str] = None


# class QuetzalCoreLogger:
    """
#     Distributed logging system for QuetzalCore
#     Way better than ELK stack - simpler, faster, smarter!
    """
    
#     def __init__(self, log_dir: str = "./logs"):
#         self.log_dir = Path(log_dir)
#         self.log_dir.mkdir(exist_ok=True)
        
#         self.logs: List[LogEntry] = []
#         self.max_memory_logs = 100000  # Keep last 100k logs in memory
        
        # Log file handles
#         self.current_log_file = None
#         self.current_date = None
        
#         logger.info(f" QuetzalCore Logger initialized: {self.log_dir}")
    
#     async def log(
#         self,
#         level: str,
#         source: str,
#         message: str,
#         context: Optional[Dict] = None,
#         trace_id: Optional[str] = None
    ):
        """Add a log entry"""
#         entry = LogEntry(
#             timestamp=datetime.now().isoformat(),
#             level=level.upper(),
#             source=source,
#             message=message,
#             context=context or {},
#             trace_id=trace_id
        
        # Add to memory buffer
#         self.logs.append(entry)
        
        # Trim if needed
#         if len(self.logs) > self.max_memory_logs:
#             self.logs = self.logs[-self.max_memory_logs:]
        
        # Write to file
#         await self._write_to_file(entry)
        
        # Check for alerts
#         if level in ['ERROR', 'CRITICAL']:
#             await self._check_alert(entry)
    
#     async def _write_to_file(self, entry: LogEntry):
        """Write log entry to daily log file"""
#         try:
#             current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Rotate log file if date changed
#             if current_date != self.current_date:
#                 if self.current_log_file:
#                     self.current_log_file.close()
                
#                 log_file_path = self.log_dir / f"quetzalcore-{current_date}.log"
#                 self.current_log_file = open(log_file_path, 'a')
#                 self.current_date = current_date
                
#                 logger.info(f" New log file: {log_file_path}")
            
            # Write log entry
#             log_line = json.dumps(asdict(entry)) + "\n"
#             self.current_log_file.write(log_line)
#             self.current_log_file.flush()
            
#         except Exception as e:
#             logger.error(f"Failed to write log: {e}")
    
#     async def _check_alert(self, entry: LogEntry):
        """Check if log entry should trigger an alert"""
        # Count recent errors from same source
#         recent_errors = [
#             log for log in self.logs[-100:]
#             if log.source == entry.source and log.level in ['ERROR', 'CRITICAL']
        ]
        
#         if len(recent_errors) > 10:
#             logger.warning(f" ALERT: High error rate from {entry.source} - {len(recent_errors)} errors")
    
#     async def search(
#         self,
#         query: Optional[str] = None,
#         level: Optional[str] = None,
#         source: Optional[str] = None,
#         start_time: Optional[datetime] = None,
#         end_time: Optional[datetime] = None,
#         limit: int = 100
    ) -> List[LogEntry]:
        """Search logs with filters"""
#         results = []
        
#         for log in reversed(self.logs):  # Most recent first
            # Apply filters
#             if level and log.level != level.upper():
#                 continue
            
#             if source and log.source != source:
#                 continue
            
#             if start_time or end_time:
#                 log_time = datetime.fromisoformat(log.timestamp)
#                 if start_time and log_time < start_time:
#                     continue
#                 if end_time and log_time > end_time:
#                     continue
            
#             if query and query.lower() not in log.message.lower():
#                 continue
            
#             results.append(log)
            
#             if len(results) >= limit:
#                 break
        
#         return results
    
#     async def get_stats(self) -> Dict:
        """Get logging statistics"""
#         now = datetime.now()
#         hour_ago = now - timedelta(hours=1)
        
#         recent_logs = [
#             log for log in self.logs
#             if datetime.fromisoformat(log.timestamp) > hour_ago
        ]
        
#         level_counts = {}
#         source_counts = {}
        
#         for log in recent_logs:
#             level_counts[log.level] = level_counts.get(log.level, 0) + 1
#             source_counts[log.source] = source_counts.get(log.source, 0) + 1
        
#         return {
            'total_logs': len(self.logs),
            'logs_last_hour': len(recent_logs),
            'level_counts': level_counts,
            'source_counts': source_counts,
            'oldest_log': self.logs[0].timestamp if self.logs else None,
            'newest_log': self.logs[-1].timestamp if self.logs else None
        }
    
#     async def rotate_and_compress(self):
        """Rotate old log files and compress them"""
#         try:
            # Find log files older than 7 days
#             cutoff_date = datetime.now() - timedelta(days=7)
            
#             for log_file in self.log_dir.glob("quetzalcore-*.log"):
                # Extract date from filename
#                 date_str = log_file.stem.split('-', 1)[1]
#                 file_date = datetime.strptime(date_str, "%Y-%m-%d")
                
#                 if file_date < cutoff_date:
                    # Compress old log file
#                     compressed_file = log_file.with_suffix('.log.gz')
                    
#                     with open(log_file, 'rb') as f_in:
#                         with gzip.open(compressed_file, 'wb') as f_out:
#                             f_out.writelines(f_in)
                    
                    # Remove original
#                     log_file.unlink()
                    
#                     logger.info(f" Compressed old log: {log_file.name}")
            
#         except Exception as e:
#             logger.error(f"Failed to rotate logs: {e}")
    
#     async def export_logs(self, output_file: str, filters: Optional[Dict] = None):
        """Export logs to a file"""
#         try:
#             logs_to_export = await self.search(**(filters or {}), limit=1000000)
            
#             with open(output_file, 'w') as f:
#                 for log in logs_to_export:
#                     f.write(json.dumps(asdict(log)) + "\n")
            
#             logger.info(f" Exported {len(logs_to_export)} logs to {output_file}")
            
#         except Exception as e:
#             logger.error(f"Failed to export logs: {e}")
    
#     def __del__(self):
        """Clean up on destruction"""
#         if self.current_log_file:
#             self.current_log_file.close()


# Singleton logger instance
_global_logger: Optional[QuetzalCoreLogger] = None


# def get_logger() -> QuetzalCoreLogger:
    """Get the global logger instance"""
#     global _global_logger
#     if _global_logger is None:
        _global_logger = QuetzalCoreLogger()
#     return _global_logger


# Convenience functions
# async def log_info(source: str, message: str, **kwargs):
    """Log an INFO message"""
#     logger_instance = get_logger()
#     await logger_instance.log('INFO', source, message, kwargs)


# async def log_warning(source: str, message: str, **kwargs):
    """Log a WARNING message"""
#     logger_instance = get_logger()
#     await logger_instance.log('WARNING', source, message, kwargs)


# async def log_error(source: str, message: str, **kwargs):
    """Log an ERROR message"""
#     logger_instance = get_logger()
#     await logger_instance.log('ERROR', source, message, kwargs)


# Example usage
# async def main():
    """Example of using the QuetzalCore logger"""
    
#     qlogger = get_logger()
    
    # Log some messages
#     await log_info("web-server", "Server started on port 8000")
#     await log_info("database", "Connected to PostgreSQL")
#     await log_warning("cache", "Redis connection slow", latency_ms=250)
#     await log_error("api", "Failed to process request", error="Connection timeout")
    
    # Wait a bit
#     await asyncio.sleep(1)
    
    # Get stats
#     stats = await qlogger.get_stats()
#     print(f"\n Logging Stats:")
#     print(json.dumps(stats, indent=2))
    
    # Search logs
#     error_logs = await qlogger.search(level='ERROR')
#     print(f"\n Found {len(error_logs)} error logs")
    
    # Export logs
#     await qlogger.export_logs("export.log", {'level': 'ERROR'})


# if __name__ == "__main__":
#     asyncio.run(main())
