
"""
Advanced Logging System for Telegram Ban-All Bot
Ultra-fast file-based logging without external dependencies
"""

import os
import json
import datetime
from typing import Dict, Any
from pathlib import Path

class PowerLogger:
    """Ultra-powerful logging system"""
    
    def __init__(self):
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create log files
        self.action_log = self.logs_dir / "actions.log"
        self.stats_log = self.logs_dir / "stats.json"
        self.error_log = self.logs_dir / "errors.log"
        
        # Initialize stats if not exists
        if not self.stats_log.exists():
            self._init_stats()
    
    def _init_stats(self):
        """Initialize stats file"""
        stats = {
            "total_operations": 0,
            "total_banned": 0,
            "total_kicked": 0,
            "total_muted": 0,
            "groups_processed": 0,
            "start_date": datetime.datetime.now().isoformat(),
            "last_operation": None
        }
        with open(self.stats_log, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def log_action(self, action: str, chat_id: int, user_id: int, details: Dict[str, Any] = None):
        """Log bot actions"""
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] ACTION: {action} | Chat: {chat_id} | User: {user_id}"
        
        if details:
            log_entry += f" | Details: {json.dumps(details)}"
        
        with open(self.action_log, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def log_operation(self, operation: str, chat_id: int, stats: Dict[str, int]):
        """Log operation results and update stats"""
        timestamp = datetime.datetime.now().isoformat()
        
        # Log to action file
        log_entry = f"[{timestamp}] OPERATION: {operation} | Chat: {chat_id} | Stats: {json.dumps(stats)}"
        with open(self.action_log, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
        
        # Update global stats
        self._update_stats(operation, stats)
    
    def log_error(self, error: str, context: str = ""):
        """Log errors"""
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] ERROR: {error}"
        if context:
            log_entry += f" | Context: {context}"
        
        with open(self.error_log, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def _update_stats(self, operation: str, stats: Dict[str, int]):
        """Update global statistics"""
        try:
            with open(self.stats_log, 'r') as f:
                global_stats = json.load(f)
            
            global_stats["total_operations"] += 1
            global_stats["groups_processed"] += 1
            global_stats["last_operation"] = datetime.datetime.now().isoformat()
            
            if "banned" in stats:
                global_stats["total_banned"] += stats["banned"]
            if "kicked" in stats:
                global_stats["total_kicked"] += stats["kicked"]
            if "muted" in stats:
                global_stats["total_muted"] += stats["muted"]
            
            with open(self.stats_log, 'w') as f:
                json.dump(global_stats, f, indent=2)
        
        except Exception:
            pass  # Silent fail for stats
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        try:
            with open(self.stats_log, 'r') as f:
                return json.load(f)
        except Exception:
            return {"error": "Stats not available"}
    
    def clear_logs(self):
        """Clear all log files"""
        for log_file in [self.action_log, self.error_log]:
            if log_file.exists():
                log_file.unlink()
        self._init_stats()

# Global logger instance
logger = PowerLogger()
