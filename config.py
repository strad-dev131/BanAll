
"""
Configuration module for Telegram Ban-All Bot
Ultra-powerful settings for the most advanced ban bot
"""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Ultra-powerful configuration class"""

    def __init__(self):
        # Telegram API credentials
        self.API_ID = int(os.getenv("API_ID", "0"))
        self.API_HASH = os.getenv("API_HASH", "")
        self.BOT_TOKEN = os.getenv("BOT_TOKEN", "")

        # Owner and Sudo users
        self.OWNER_ID = int(os.getenv("OWNER_ID", "0"))
        sudo_users_str = os.getenv("SUDO_USERS", "")
        self.SUDO_USERS = [int(user_id.strip()) for user_id in sudo_users_str.split(",") if user_id.strip()]

        # Add owner to sudo users if specified
        if self.OWNER_ID and self.OWNER_ID not in self.SUDO_USERS:
            self.SUDO_USERS.append(self.OWNER_ID)

        # Ultra-powerful bot settings
        self.MAX_CONCURRENT_OPERATIONS = int(os.getenv("MAX_CONCURRENT_OPERATIONS", "15"))
        self.FLOOD_WAIT_THRESHOLD = int(os.getenv("FLOOD_WAIT_THRESHOLD", "25"))
        self.OPERATION_DELAY = float(os.getenv("OPERATION_DELAY", "0.05"))  # Delay between operations
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))  # Members per batch
        
        # Advanced features
        self.AUTO_LEAVE_AFTER_BAN = os.getenv("AUTO_LEAVE_AFTER_BAN", "true").lower() == "true"
        self.AUTO_LEAVE_AFTER_KICK = os.getenv("AUTO_LEAVE_AFTER_KICK", "true").lower() == "true"
        self.STEALTH_MODE = os.getenv("STEALTH_MODE", "true").lower() == "true"  # Minimal messages
        self.DELETE_COMMANDS = os.getenv("DELETE_COMMANDS", "true").lower() == "true"  # Delete command messages
        
        # Security features
        self.PROTECTED_USERS = self._parse_protected_users()
        self.BYPASS_ADMIN_CHECK = os.getenv("BYPASS_ADMIN_CHECK", "false").lower() == "true"
        
        # Performance optimization
        self.USE_CACHE = os.getenv("USE_CACHE", "true").lower() == "true"
        self.CACHE_DURATION = int(os.getenv("CACHE_DURATION", "300"))  # 5 minutes
        
        # Validate required settings
        self._validate_config()

    def _parse_protected_users(self) -> List[int]:
        """Parse protected users from environment"""
        protected_str = os.getenv("PROTECTED_USERS", "")
        if not protected_str:
            return []
        
        protected_users = []
        for user_id in protected_str.split(","):
            try:
                protected_users.append(int(user_id.strip()))
            except ValueError:
                continue
        return protected_users

    def _validate_config(self):
        """Validate that all required configuration is present"""
        if not self.API_ID or self.API_ID == 0:
            raise ValueError("API_ID is required and must be a valid integer")

        if not self.API_HASH:
            raise ValueError("API_HASH is required")

        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")

        if not self.SUDO_USERS:
            raise ValueError("SUDO_USERS is required and must contain at least one user ID")

    def is_sudo_user(self, user_id: int) -> bool:
        """Check if user ID is in sudo users list"""
        return user_id in self.SUDO_USERS
    
    def is_protected_user(self, user_id: int) -> bool:
        """Check if user is protected from actions"""
        return user_id in self.PROTECTED_USERS or user_id in self.SUDO_USERS
