"""
Chatbot Handler for BanAll Bot with OpenRouterClient integration
Handles normal user conversations asynchronously with context and retries
"""

import datetime
from typing import List, Dict
from pyrogram import Client
from pyrogram.types import Message
from utils.logger import logger
from config import Config
from utils.openrouter import OpenRouterClient

class ChatbotHandler:
    def __init__(self, app: Client, config: Config, utils, logger):
        self.app = app
        self.config = config
        self.utils = utils
        self.logger = logger

        self.openrouter_client = OpenRouterClient(config)

        # Conversation state: user_id -> list of messages [{"role":..., "content":...}]
        self.conversations: Dict[int, List[Dict[str, str]]] = {}

        # Conversation expiration time in seconds (1 hour)
        self.conversation_expiry = 3600

        # Timestamps for last activity per user: user_id -> datetime
        self.last_activity: Dict[int, datetime.datetime] = {}

    async def handle_message(self, message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id

        if not self.config.CHATBOT_ENABLED or not self.utils.can_use_chatbot(user_id):
            return

        # Clean expired conversations
        self._cleanup_expired_conversations()

        user_input = message.text.strip()
        user_messages = self.conversations.get(user_id, [])

        user_messages.append({"role": "user", "content": user_input})

        # Prepare payload messages with system prompt + conversation history (max 10 messages)
        messages_payload = [
            {"role": "system", "content": "You are ChatMate, a friendly and helpful AI assistant."}
        ] + user_messages[-10:]

        try:
            # Query OpenRouter API via client utility
            response = await self.openrouter_client.send_chat_request(messages_payload)

            if not response:
                response = "Sorry, I am having trouble right now. Please try again later."

            # Log AI response and update conversation
            self.logger.log_action("CHATBOT_RESPONSE", chat_id, user_id, {"reply": response})
            user_messages.append({"role": "assistant", "content": response})

            # Update conversation state and timestamp
            self.conversations[user_id] = user_messages[-10:]
            self.last_activity[user_id] = datetime.datetime.utcnow()

            # Send AI response back to user
            await message.reply_text(response)

        except Exception as exc:
            self.logger.log_error(f"Chatbot handle_message error: {exc}", f"User: {user_id} Chat: {chat_id}")
            await message.reply_text("Oops! Something went wrong on my side. Please try again later.")

    def _cleanup_expired_conversations(self):
        """Remove conversations inactive beyond expiration time to save memory."""
        now = datetime.datetime.utcnow()
        expired_users = [uid for uid, last_time in self.last_activity.items()
                         if (now - last_time).total_seconds() > self.conversation_expiry]

        for uid in expired_users:
            self.conversations.pop(uid, None)
            self.last_activity.pop(uid, None)
            self.logger.log_action("CHATBOT_CONV_CLEANUP", 0, uid)

