
"""
🔥 ULTRA-POWERFUL BAN HANDLERS 🔥
Advanced ban and mute operations with military precision
"""

import asyncio
from typing import List
from pyrogram import Client
from pyrogram.types import Message, ChatMember, ChatPermissions
from pyrogram.errors import FloodWait, ChatAdminRequired, UserAdminInvalid, PeerIdInvalid
from config import Config
from handlers.utils import Utils

class BanHandler:
    """Ultra-powerful handler for ban and mute operations"""

    def __init__(self, app: Client, config: Config, utils: Utils, logger):
        self.app = app
        self.config = config
        self.utils = utils
        self.logger = logger

    async def ban_all_members(self, message: Message):
        """🔥 BAN ALL MEMBERS - ULTRA POWERFUL 🔥"""
        # Check sudo permissions
        if not self.utils.is_sudo_user(message.from_user.id):
            await message.reply_text("🚫 **ACCESS DENIED!** Only SUDO users can use this ULTRA command.")
            return

        # Delete command message for stealth
        await self.utils.delete_message_safe(message)

        # Check bot permissions
        if not await self.utils.check_bot_permissions(message.chat.id):
            await message.reply_text("❌ **ERROR!** Bot needs ADMIN permissions for ULTRA BAN operation.")
            return

        try:
            # Send initial stealth message
            if not self.config.STEALTH_MODE:
                status_message = await message.reply_text("🔥 **ULTRA BAN-ALL OPERATION INITIATED...**\n\n⚡ Fetching targets...")
            else:
                status_message = None

            # Get all members with caching
            members = await self.utils.get_all_members(message.chat.id)
            if not members:
                if status_message:
                    await status_message.edit_text("❌ **ERROR!** Could not fetch group members.")
                return

            # Filter actionable members with advanced protection
            actionable_members = await self.utils.filter_actionable_members(message.chat.id, members)

            if not actionable_members:
                if status_message:
                    await status_message.edit_text("ℹ️ **NO TARGETS!** All members are protected or admins.")
                await asyncio.sleep(2)
                if self.config.AUTO_LEAVE_AFTER_BAN:
                    await self.utils.leave_chat(message.chat.id)
                return

            if status_message:
                await status_message.edit_text(f"🔥 **BANNING {len(actionable_members)} TARGETS...**\n⚡ ULTRA SPEED MODE ENGAGED!")

            # Ultra-powerful concurrent banning
            banned_count = 0
            failed_count = 0
            semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_OPERATIONS)

            async def ultra_ban_member(member: ChatMember):
                nonlocal banned_count, failed_count
                async with semaphore:
                    try:
                        await self.utils.handle_flood_wait(
                            self.app.ban_chat_member,
                            message.chat.id,
                            member.user.id
                        )
                        banned_count += 1
                        self.logger.log_action("MEMBER_BANNED", message.chat.id, member.user.id)
                    except Exception as e:
                        failed_count += 1
                        self.logger.log_error(f"Ban failed for user {member.user.id}: {str(e)}")

                    # Ultra-fast operation delay
                    await asyncio.sleep(self.config.OPERATION_DELAY)

            # Execute ultra-fast concurrent bans
            tasks = [ultra_ban_member(member) for member in actionable_members]
            await asyncio.gather(*tasks, return_exceptions=True)

            # Log operation results
            operation_stats = {
                "banned": banned_count,
                "failed": failed_count,
                "total_processed": len(actionable_members)
            }
            self.logger.log_operation("BAN_ALL", message.chat.id, operation_stats)

            # Final status
            if not self.config.STEALTH_MODE:
                result_text = f"🔥 **ULTRA BAN-ALL OPERATION COMPLETED!** 🔥\n\n"
                result_text += f"**✅ BANNED:** {banned_count} targets\n"
                result_text += f"**❌ FAILED:** {failed_count} targets\n"
                result_text += f"**⚡ TOTAL PROCESSED:** {len(actionable_members)} targets\n\n"
                
                if self.config.AUTO_LEAVE_AFTER_BAN:
                    result_text += f"**🚪 LEAVING CHAT IN 3 SECONDS...**\n🔥 NO TRACES LEFT BEHIND!"

                if status_message:
                    await status_message.edit_text(result_text)

            # Auto-leave for stealth
            if self.config.AUTO_LEAVE_AFTER_BAN:
                await asyncio.sleep(3)
                await self.utils.leave_chat(message.chat.id)

        except Exception as e:
            self.logger.log_error(f"Ban-all operation failed: {str(e)}", f"Chat: {message.chat.id}")
            if not self.config.STEALTH_MODE:
                await message.reply_text("❌ **ERROR during ULTRA BAN operation!**")
            if self.config.AUTO_LEAVE_AFTER_BAN:
                await asyncio.sleep(2)
                await self.utils.leave_chat(message.chat.id)

    async def nuke_all_members(self, message: Message):
        """🔥 NUKE ALL - ULTIMATE DESTRUCTION 🔥"""
        if not self.utils.is_sudo_user(message.from_user.id):
            await message.reply_text("🚫 **ACCESS DENIED!** Only SUDO users can use NUKE command.")
            return

        await self.utils.delete_message_safe(message)

        if not await self.utils.check_bot_permissions(message.chat.id):
            await message.reply_text("❌ **ERROR!** Bot needs ADMIN permissions for NUKE operation.")
            return

        try:
            # Send warning
            warning_msg = await message.reply_text("⚠️ **NUKE MODE ACTIVATED!**\n🔥 **ULTIMATE DESTRUCTION IN 5 SECONDS!**")
            await asyncio.sleep(5)

            # First ban all members
            await self.ban_all_members(message)

            # Then try to delete recent messages (if possible)
            try:
                async for msg in self.app.get_chat_history(message.chat.id, limit=100):
                    try:
                        await msg.delete()
                        await asyncio.sleep(0.1)
                    except:
                        continue
            except:
                pass

            self.logger.log_operation("NUKE_ALL", message.chat.id, {"operation": "complete_destruction"})

        except Exception as e:
            self.logger.log_error(f"Nuke operation failed: {str(e)}", f"Chat: {message.chat.id}")

    async def unban_all_members(self, message: Message):
        """Unban all banned members from the group"""
        if not self.utils.is_sudo_user(message.from_user.id):
            await message.reply_text("🚫 **ACCESS DENIED!** Only SUDO users can use this command.")
            return

        await self.utils.delete_message_safe(message)

        if not await self.utils.check_bot_permissions(message.chat.id):
            await message.reply_text("❌ **ERROR!** Bot needs admin permissions to unban members.")
            return

        try:
            status_message = await message.reply_text("🔄 **Starting ULTRA Unban-All Operation...**")

            # Note: Telegram doesn't provide a direct way to get all banned members
            await status_message.edit_text(
                "ℹ️ **UNBAN-ALL NOTICE**\n\n"
                "Due to Telegram API limitations, we cannot fetch the list of banned members.\n"
                "To unban specific users, contact them directly or use their user IDs."
            )

            self.logger.log_action("UNBAN_ALL_ATTEMPTED", message.chat.id, message.from_user.id)

        except Exception as e:
            self.logger.log_error(f"Unban operation failed: {str(e)}")

    async def mute_all_members(self, message: Message):
        """🔇 MUTE ALL MEMBERS - SILENCE PROTOCOL 🔇"""
        if not self.utils.is_sudo_user(message.from_user.id):
            await message.reply_text("🚫 **ACCESS DENIED!** Only SUDO users can use MUTE command.")
            return

        await self.utils.delete_message_safe(message)

        if not await self.utils.check_bot_permissions(message.chat.id):
            await message.reply_text("❌ **ERROR!** Bot needs admin permissions to mute members.")
            return

        try:
            status_message = await message.reply_text("🔇 **ULTRA MUTE-ALL OPERATION INITIATED...**")

            # Get all members
            members = await self.utils.get_all_members(message.chat.id)
            actionable_members = await self.utils.filter_actionable_members(message.chat.id, members)

            if not actionable_members:
                await status_message.edit_text("ℹ️ **NO TARGETS!** All members are admins or protected.")
                return

            # Ultra-restrictive mute permissions
            mute_permissions = ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_send_polls=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )

            muted_count = 0
            failed_count = 0
            semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_OPERATIONS)

            async def ultra_mute_member(member: ChatMember):
                nonlocal muted_count, failed_count
                async with semaphore:
                    try:
                        await self.utils.handle_flood_wait(
                            self.app.restrict_chat_member,
                            message.chat.id,
                            member.user.id,
                            mute_permissions
                        )
                        muted_count += 1
                        self.logger.log_action("MEMBER_MUTED", message.chat.id, member.user.id)
                    except Exception:
                        failed_count += 1

                    await asyncio.sleep(self.config.OPERATION_DELAY)

            # Execute ultra-fast concurrent mutes
            tasks = [ultra_mute_member(member) for member in actionable_members]
            await asyncio.gather(*tasks, return_exceptions=True)

            operation_stats = {"muted": muted_count, "failed": failed_count}
            self.logger.log_operation("MUTE_ALL", message.chat.id, operation_stats)

            result_text = f"🔇 **ULTRA MUTE-ALL COMPLETED!** 🔇\n\n"
            result_text += f"**🔇 MUTED:** {muted_count} targets\n"
            result_text += f"**❌ FAILED:** {failed_count} targets\n"
            result_text += f"**⚡ TOTAL PROCESSED:** {len(actionable_members)} targets"

            await status_message.edit_text(result_text)

        except Exception as e:
            self.logger.log_error(f"Mute-all operation failed: {str(e)}")

    async def unmute_all_members(self, message: Message):
        """🔊 UNMUTE ALL MEMBERS - RESTORE VOICES 🔊"""
        if not self.utils.is_sudo_user(message.from_user.id):
            await message.reply_text("🚫 **ACCESS DENIED!** Only SUDO users can use UNMUTE command.")
            return

        await self.utils.delete_message_safe(message)

        if not await self.utils.check_bot_permissions(message.chat.id):
            await message.reply_text("❌ **ERROR!** Bot needs admin permissions to unmute members.")
            return

        try:
            status_message = await message.reply_text("🔊 **ULTRA UNMUTE-ALL OPERATION INITIATED...**")

            # Get all members
            members = await self.utils.get_all_members(message.chat.id)
            actionable_members = await self.utils.filter_actionable_members(message.chat.id, members)

            # Full permissions (restore everything)
            default_permissions = ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )

            unmuted_count = 0
            failed_count = 0
            semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_OPERATIONS)

            async def ultra_unmute_member(member: ChatMember):
                nonlocal unmuted_count, failed_count
                async with semaphore:
                    try:
                        await self.utils.handle_flood_wait(
                            self.app.restrict_chat_member,
                            message.chat.id,
                            member.user.id,
                            default_permissions
                        )
                        unmuted_count += 1
                        self.logger.log_action("MEMBER_UNMUTED", message.chat.id, member.user.id)
                    except Exception:
                        failed_count += 1

                    await asyncio.sleep(self.config.OPERATION_DELAY)

            # Execute ultra-fast concurrent unmutes
            tasks = [ultra_unmute_member(member) for member in actionable_members]
            await asyncio.gather(*tasks, return_exceptions=True)

            operation_stats = {"unmuted": unmuted_count, "failed": failed_count}
            self.logger.log_operation("UNMUTE_ALL", message.chat.id, operation_stats)

            result_text = f"🔊 **ULTRA UNMUTE-ALL COMPLETED!** 🔊\n\n"
            result_text += f"**🔊 UNMUTED:** {unmuted_count} targets\n"
            result_text += f"**❌ FAILED:** {failed_count} targets\n"
            result_text += f"**⚡ TOTAL PROCESSED:** {len(actionable_members)} targets"

            await status_message.edit_text(result_text)

        except Exception as e:
            self.logger.log_error(f"Unmute-all operation failed: {str(e)}")
