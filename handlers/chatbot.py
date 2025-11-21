"""
Chatbot Handler - Production Grade with Full Debugging
"""

import datetime
from typing import List, Dict
from pyrogram import Client
from pyrogram.types import Message
from utils.logger import logger
from config import Config
from utils.openrouter import OpenRouterClient


class ChatbotHandler:
    def __init__(self, app: Client, config: Config, utils, logger_instance):
        self.app = app
        self.config = config
        self.utils = utils
        self.logger = logger_instance
        self.openrouter_client = OpenRouterClient(config)
        self.conversations: Dict[int, List[Dict[str, str]]] = {}
        self.conversation_expiry = 3600
        self.last_activity: Dict[int, datetime.datetime] = {}

    async def handle_message(self, message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        username = message.from_user.username or message.from_user.first_name or "friend"

        self.logger.log_action("CHATBOT_MESSAGE_RECEIVED", chat_id, user_id, {
            "text_preview": message.text[:50] if message.text else "no_text"
        })

        if not self.config.CHATBOT_ENABLED:
            self.logger.log_action("CHATBOT_DISABLED", chat_id, user_id)
            return

        if not self.utils.can_use_chatbot(user_id):
            self.logger.log_action("CHATBOT_USER_NOT_ALLOWED", chat_id, user_id)
            return

        self._cleanup_expired_conversations()

        user_input = message.text.strip()
        user_messages = self.conversations.get(user_id, [])
        user_messages.append({"role": "user", "content": user_input})

        system_prompt = (
            f"You are ChatMate, a friendly AI assistant chatting with {username}. "
            "Keep responses SHORT (1-3 sentences), natural, and conversational. "
            "Use emojis occasionally. Be helpful and engaging."
        )

        messages_payload = [{"role": "system", "content": system_prompt}] + user_messages[-8:]

        self.logger.log_action("CHATBOT_CALLING_API", chat_id, user_id, {
            "payload_size": len(messages_payload)
        })

        try:
            response = await self.openrouter_client.send_chat_request(messages_payload)

            self.logger.log_action("CHATBOT_API_RETURNED", chat_id, user_id, {
                "response_empty": not bool(response),
                "response_length": len(response) if response else 0
            })

            if not response:
                # Enhanced fallback
                response = "Hmm, I'm drawing a blank here! 😅 Try asking me something else?"
                self.logger.log_action("CHATBOT_USING_FALLBACK", chat_id, user_id)

            user_messages.append({"role": "assistant", "content": response})
            self.conversations[user_id] = user_messages[-8:]
            self.last_activity[user_id] = datetime.datetime.utcnow()

            await message.reply_text(response)
            
            self.logger.log_action("CHATBOT_RESPONSE_SENT", chat_id, user_id, {
                "response_preview": response[:50]
            })

        except Exception as exc:
            self.logger.log_error(f"Chatbot handler exception: {type(exc).__name__} - {str(exc)}")
            await message.reply_text("Oops! Something went wrong 🤖 Try again?")

    def _cleanup_expired_conversations(self):
        now = datetime.datetime.utcnow()
        expired = [uid for uid, last_time in self.last_activity.items()
                   if (now - last_time).total_seconds() > self.conversation_expiry]
        for uid in expired:
            self.conversations.pop(uid, None)
            self.last_activity.pop(uid, None)
