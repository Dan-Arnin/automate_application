"""
Logging setup module for structured logging across the application.
Provides separate loggers for application events and system events.
"""

import logging
from logging.handlers import RotatingFileHandler
import sys
from config import Config

# Custom log format with timestamp, level, and message
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name, log_file, level=None):
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level (defaults to Config.LOG_LEVEL)
    
    Returns:
        Configured logger instance
    """
    if level is None:
        level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=Config.LOG_MAX_BYTES,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create default loggers
application_logger = setup_logger(
    "application",
    Config.APPLICATION_LOG_FILE
)

system_logger = setup_logger(
    "system",
    Config.SYSTEM_LOG_FILE
)

def get_application_logger():
    """Get the application events logger."""
    return application_logger

def get_system_logger():
    """Get the system events logger."""
    return system_logger
