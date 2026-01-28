import os
import sys
import logging
from datetime import datetime

# Add project root to path FIRST
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

#Import  Path_Utilis FIRST to fix Python Path 
from eti_pipeline.src.utilis.path_utilis import PROJECT_ROOT

#Import from config 
from config.config import (
    LOG_FORMAT,
    LOG_LEVEL
)


def setup_logging(name: str = None) -> logging.Logger:
    """Configure and return with consistent formatting
       Creates timestamped log files in logs/ directory.
       Console shows INFO+, file captures DEBUG+.
    
    """

    # Create logs directory if it doesn't exist
    log_dir = os.path.join(PROJECT_ROOT, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create timestamped log filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'pipeline_{timestamp}.log'
    log_filepath = os.path.join(log_dir, log_filename)
    
    # Clear any existing handlers (prevents duplicate logs)
    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.handlers.clear()


    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            
            # Handler 1: Console (shows INFO and above)
            logging.StreamHandler(),
            # Handler 2: File (captures everything including DEBUG)
            logging.FileHandler(log_filepath, mode='w', encoding='utf-8')
            ]
    )

    logger = logging.getLogger(name)
    logger.info(f" Log file created: {log_filename}")
    return logger

# Test the logger setup

if __name__ == "__main__":
    logger = setup_logging(__name__)
    logger.info("Logger utility is working!")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")

