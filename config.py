"""
Configuration module for job application automation system.
Centralizes all configuration settings for easy management.
"""

import os
from pathlib import Path

class Config:
    """Configuration settings for the job application automation system."""
    
    # Project paths
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"
    
    # Ensure directories exist
    LOGS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    APPLICATION_LOG_FILE = LOGS_DIR / "applications.log"
    SYSTEM_LOG_FILE = LOGS_DIR / "system.log"
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Application tracking
    APPLICATION_HISTORY_FILE = DATA_DIR / "applications.json"
    
    # Error handling and retry configuration
    MAX_RETRY_ATTEMPTS = 3
    RETRY_BACKOFF_MULTIPLIER = 2  # Exponential backoff: 1s, 2s, 4s, etc.
    INITIAL_RETRY_DELAY = 1  # seconds
    
    # Browser automation settings
    PAGE_LOAD_TIMEOUT = 30  # seconds
    ELEMENT_WAIT_TIMEOUT = 10  # seconds
    
    # Form filling settings
    TYPING_DELAY = 0.1  # seconds between keystrokes (more human-like)
    CLICK_DELAY = 0.5  # seconds after clicking
    
    # Application settings
    PREVENT_DUPLICATE_APPLICATIONS = True
    AUTO_SAVE_PROGRESS = True
    
    @classmethod
    def get_config_summary(cls):
        """Return a summary of current configuration."""
        return {
            "logs_dir": str(cls.LOGS_DIR),
            "data_dir": str(cls.DATA_DIR),
            "log_level": cls.LOG_LEVEL,
            "max_retries": cls.MAX_RETRY_ATTEMPTS,
            "prevent_duplicates": cls.PREVENT_DUPLICATE_APPLICATIONS,
        }
