"""
Application tracking module for managing job application state and history.
Tracks application status, prevents duplicates, and maintains history.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List
from pathlib import Path
from logger_setup import get_application_logger
from config import Config

logger = get_application_logger()

class ApplicationStatus(Enum):
    """Status of a job application."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_MANUAL = "requires_manual"

class ApplicationTracker:
    """Tracks job applications and maintains history."""
    
    def __init__(self, history_file: Optional[Path] = None):
        """
        Initialize the application tracker.
        
        Args:
            history_file: Path to the history file (defaults to Config.APPLICATION_HISTORY_FILE)
        """
        self.history_file = history_file or Config.APPLICATION_HISTORY_FILE
        self.applications = self._load_history()
    
    def _load_history(self) -> Dict:
        """Load application history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data)} applications from history")
                    return data
            except Exception as e:
                logger.error(f"Error loading history: {e}")
                return {}
        return {}
    
    def _save_history(self):
        """Save application history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.applications, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.applications)} applications to history")
        except Exception as e:
            logger.error(f"Error saving history: {e}")
    
    def add_application(
        self,
        url: str,
        company: str,
        position: str,
        status: ApplicationStatus = ApplicationStatus.PENDING,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Add a new application to tracking.
        
        Args:
            url: Job application URL
            company: Company name
            position: Job position/title
            status: Initial status
            metadata: Additional metadata
        
        Returns:
            Application ID
        """
        app_id = self._generate_app_id(url)
        
        # Check for duplicates if enabled
        if Config.PREVENT_DUPLICATE_APPLICATIONS and app_id in self.applications:
            existing = self.applications[app_id]
            logger.warning(f"Duplicate application detected: {company} - {position}")
            logger.warning(f"Previous application on {existing['created_at']} with status {existing['status']}")
            return app_id
        
        application = {
            "id": app_id,
            "url": url,
            "company": company,
            "position": position,
            "status": status.value,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "attempts": 0,
            "errors": []
        }
        
        self.applications[app_id] = application
        
        if Config.AUTO_SAVE_PROGRESS:
            self._save_history()
        
        logger.info(f"Added application: {company} - {position} (ID: {app_id})")
        return app_id
    
    def update_status(
        self,
        app_id: str,
        status: ApplicationStatus,
        error_info: Optional[Dict] = None
    ):
        """
        Update application status.
        
        Args:
            app_id: Application ID
            status: New status
            error_info: Error information if status is FAILED
        """
        if app_id not in self.applications:
            logger.error(f"Application {app_id} not found")
            return
        
        app = self.applications[app_id]
        old_status = app["status"]
        app["status"] = status.value
        app["updated_at"] = datetime.now().isoformat()
        
        if error_info:
            app["errors"].append({
                "timestamp": datetime.now().isoformat(),
                "error": error_info
            })
        
        if Config.AUTO_SAVE_PROGRESS:
            self._save_history()
        
        logger.info(f"Updated application {app_id}: {old_status} -> {status.value}")
    
    def increment_attempts(self, app_id: str):
        """Increment the number of attempts for an application."""
        if app_id in self.applications:
            self.applications[app_id]["attempts"] += 1
            self.applications[app_id]["updated_at"] = datetime.now().isoformat()
            
            if Config.AUTO_SAVE_PROGRESS:
                self._save_history()
    
    def get_application(self, app_id: str) -> Optional[Dict]:
        """Get application by ID."""
        return self.applications.get(app_id)
    
    def get_applications_by_status(self, status: ApplicationStatus) -> List[Dict]:
        """Get all applications with a specific status."""
        return [
            app for app in self.applications.values()
            if app["status"] == status.value
        ]
    
    def is_duplicate(self, url: str) -> bool:
        """Check if an application URL has already been applied to."""
        app_id = self._generate_app_id(url)
        return app_id in self.applications
    
    def get_statistics(self) -> Dict:
        """Get application statistics."""
        stats = {
            "total": len(self.applications),
            "by_status": {}
        }
        
        for status in ApplicationStatus:
            count = len(self.get_applications_by_status(status))
            stats["by_status"][status.value] = count
        
        return stats
    
    def export_to_csv(self, output_file: Path):
        """Export applications to CSV file."""
        import csv
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if not self.applications:
                    return
                
                fieldnames = ["id", "company", "position", "url", "status", 
                             "created_at", "updated_at", "attempts"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for app in self.applications.values():
                    row = {k: app.get(k, "") for k in fieldnames}
                    writer.writerow(row)
            
            logger.info(f"Exported {len(self.applications)} applications to {output_file}")
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
    
    def _generate_app_id(self, url: str) -> str:
        """Generate a unique application ID from URL."""
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()[:12]
    
    def save(self):
        """Manually save the current state."""
        self._save_history()
