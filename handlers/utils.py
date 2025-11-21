"""
Ultra-Powerful Utility functions for Telegram Ban-All Bot
Advanced helpers with caching and optimization
"""

import asyncio
import time
from typing import List
from pyrogram import Client
from pyrogram.types import Message, ChatMember
from pyrogram.errors import FloodWait
from config import Config

class Utils:
    """Ultra-powerful utility class with advanced functionality"""

    def __init__(self, app: Client, config: Config, logger):
        self.app = app
        self.config = config
        self.logger = logger
        self.member_cache = {}  # Cache for member lists
        self.admin_cache = {}   # Cache for admin status

    def is_sudo_user(self, user_id: int) -> bool:
        """Check if user is authorized sudo user"""
        return user_id in self.config.SUDO_USERS

    def can_use_chatbot(self, user_id: int) -> bool:
        """Check if user is allowed to use chatbot feature (non-sudo)"""
        return not self.is_sudo_user(user_id)

    async def send_sudo_only_message(self, message: Message, response: str):
        """Send message only if user is sudo"""
        if not self.is_sudo_user(message.from_user.id):
            await message.reply_text("🚫 **ACCESS DENIED!** This bot is SUDO-ONLY.")
            self.logger.log_action("ACCESS_DENIED", message.chat.id, message.from_user.id)
            return
        await message.reply_text(response)

    async def check_bot_permissions(self, chat_id: int) -> bool:
        """Check if bot has admin permissions in the chat"""
        try:
            bot_member = await self.app.get_chat_member(chat_id, "me")
            has_perms = bot_member.privileges and (
                bot_member.privileges.can_restrict_members or
                bot_member.privileges.can_delete_messages
            )
            self.logger.log_action("PERMISSION_CHECK", chat_id, 0, {"has_permissions": has_perms})
            return has_perms
        except Exception as e:
            self.logger.log_error(f"Permission check failed: {str(e)}", f"Chat: {chat_id}")
            return False

    async def is_user_admin(self, chat_id: int, user_id: int) -> bool:
        """Check if user is admin in the chat with caching"""
        cache_key = f"{chat_id}_{user_id}"
        
        if self.config.USE_CACHE and cache_key in self.admin_cache:
            cache_data = self.admin_cache[cache_key]
            if time.time() - cache_data["timestamp"] < self.config.CACHE_DURATION:
                return cache_data["is_admin"]
        
        try:
            member = await self.app.get_chat_member(chat_id, user_id)
            is_admin = member.status in ["creator", "administrator"]
            
            if self.config.USE_CACHE:
                self.admin_cache[cache_key] = {
                    "is_admin": is_admin,
                    "timestamp": time.time()
                }
            
            return is_admin
        except Exception:
            return False

    async def get_all_members(self, chat_id: int) -> List[ChatMember]:
        """Get all members from a chat with advanced caching"""
        cache_key = str(chat_id)
        
        if self.config.USE_CACHE and cache_key in self.member_cache:
            cache_data = self.member_cache[cache_key]
            if time.time() - cache_data["timestamp"] < self.config.CACHE_DURATION:
                self.logger.log_action("CACHE_HIT", chat_id, 0, {"members_count": len(cache_data["members"])})
                return cache_data["members"]
        
        members = []
        try:
            async for member in self.app.get_chat_members(chat_id):
                members.append(member)
            
            if self.config.USE_CACHE:
                self.member_cache[cache_key] = {
                    "members": members,
                    "timestamp": time.time()
                }
            
            self.logger.log_action("MEMBERS_FETCHED", chat_id, 0, {"count": len(members)})
            return members
        except Exception as e:
            self.logger.log_error(f"Failed to fetch members: {str(e)}", f"Chat: {chat_id}")
            return []

    async def filter_actionable_members(self, chat_id: int, members: List[ChatMember]) -> List[ChatMember]:
        """Filter members that can be acted upon with advanced protection"""
        actionable_members = []
        bot_info = await self.app.get_me()
        
        protected_count = 0
        bot_count = 0
        admin_count = 0

        for member in members:
            # Skip if user is creator or admin
            if member.status in ["creator", "administrator"]:
                admin_count += 1
                continue

            # Skip if user is the bot itself
            if member.user.id == bot_info.id:
                bot_count += 1
                continue

            # Skip if user is sudo user or protected
            if self.config.is_protected_user(member.user.id):
                protected_count += 1
                continue

            # Skip deleted accounts
            if member.user.is_deleted:
                continue

            # Skip bots (optional)
            if member.user.is_bot:
                bot_count += 1
                continue

            actionable_members.append(member)

        self.logger.log_action("MEMBER_FILTERING", chat_id, 0, {
            "total_members": len(members),
            "actionable": len(actionable_members),
            "protected": protected_count,
            "admins": admin_count,
            "bots": bot_count
        })

        return actionable_members

    async def handle_flood_wait(self, func, *args, **kwargs):
        """Handle FloodWait errors with advanced retry mechanism"""
        max_retries = 5
        base_delay = 1

        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except FloodWait as e:
                if attempt == max_retries - 1:
                    self.logger.log_error(f"FloodWait max retries reached: {e.value}s")
                    raise

                wait_time = min(e.value, self.config.FLOOD_WAIT_THRESHOLD)
                self.logger.log_action("FLOOD_WAIT", 0, 0, {"wait_time": wait_time, "attempt": attempt + 1})
                await asyncio.sleep(wait_time)
                
                # Exponential backoff
                base_delay *= 2
                
            except Exception as e:
                self.logger.log_error(f"Operation failed: {str(e)}")
                raise

    async def leave_chat(self, chat_id: int):
        """Leave the chat with logging"""
        try:
            await self.app.leave_chat(chat_id)
            self.logger.log_action("CHAT_LEFT", chat_id, 0)
        except Exception as e:
            self.logger.log_error(f"Failed to leave chat: {str(e)}", f"Chat: {chat_id}")

    async def delete_message_safe(self, message: Message):
        """Safely delete a message"""
        if self.config.DELETE_COMMANDS:
            try:
                await message.delete()
                self.logger.log_action("MESSAGE_DELETED", message.chat.id, message.from_user.id)
            except Exception:
                pass  # Silent fail

    async def send_stealth_message(self, chat_id: int, text: str, duration: int = 5):
        """Send a message that auto-deletes for stealth mode"""
        try:
            if self.config.STEALTH_MODE:
                msg = await self.app.send_message(chat_id, text)
                await asyncio.sleep(duration)
                try:
                    await msg.delete()
                except:
                    pass
            else:
                await self.app.send_message(chat_id, text)
        except Exception:
            pass

    def clear_cache(self):
        """Clear all caches"""
        self.member_cache.clear()
        self.admin_cache.clear()
        self.logger.log_action("CACHE_CLEARED", 0, 0)
