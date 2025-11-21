"""
Chatbot Handler for BanAll Bot
Handles normal user conversations via OpenRouter AI chat model
"""

import aiohttp
import asyncio
import datetime
from typing import List, Dict, Any
from pyrogram import Client
from pyrogram.types import Message
from utils.logger import logger
from config import Config

class ChatbotHandler:
    def __init__(self, app: Client, config: Config, utils, logger):
        self.app = app
        self.config = config
        self.utils = utils
        self.logger = logger
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.token_limit = 160000  # generous context limit for model

        # In-memory conversation state cache {user_id: [messages...]}
        self.conversations: Dict[int, List[Dict[str, str]]] = {}

        # Conversation expiration in seconds (1 hour)
        self.conversation_expiry = 3600

    async def handle_message(self, message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id

        # Only handle if chatbot enabled and user allowed
        if not self.config.CHATBOT_ENABLED or not self.utils.can_use_chatbot(user_id):
            return

        # Initialize or cleanup conversation context
        self._cleanup_expired_conversations()

        # Prepare conversation context
        user_messages = self.conversations.get(user_id, [])
        user_input = message.text.strip()

        user_messages.append({"role": "user", "content": user_input})
        self.conversations[user_id] = user_messages[-10:]  # keep last 10 messages max

        # Build request payload for OpenRouter API
        payload = {
            "model": self.config.CHATBOT_MODEL,
            "messages": [
                {"role": "system", "content": "You are ChatMate, a friendly and helpful AI assistant."}
            ] + user_messages
        }

        try:
            response_msg = await self._query_openrouter(payload)
            if not response_msg:
                response_msg = "Sorry, I am having trouble right now. Please try again later."

            # Log the conversation response
            self.logger.log_action("CHATBOT_RESPONSE", chat_id, user_id, {"reply": response_msg})

            # Update conversation context with assistant reply
            self.conversations[user_id].append({"role": "assistant", "content": response_msg})
            self.conversations[user_id] = self.conversations[user_id][-10:]  # maintain max length

            await message.reply_text(response_msg)

        except Exception as e:
            self.logger.log_error(f"Chatbot API error: {str(e)}", f"User: {user_id}, Chat: {chat_id}")
            await message.reply_text("Oops! Something went wrong on my side. Please try again later.")

    async def _query_openrouter(self, payload: dict) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.OPENROUTER_API_KEY}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload, headers=headers, timeout=30) as resp:
                if resp.status == 200:
                    json_resp = await resp.json()
                    return self._extract_response(json_resp)
                else:
                    self.logger.log_error(f"OpenRouter API returned status {resp.status}")
                    return ""

    def _extract_response(self, api_response: dict) -> str:
        """
        Extracts the assistant's reply from OpenRouter API response.
        Handles various response formats gracefully.
        """
        try:
            choices = api_response.get("choices", [])
            if choices and isinstance(choices, list):
                message_obj = choices[0].get("message", {})
                content = message_obj.get("content", "")
                return content.strip()
            return ""
        except Exception as e:
            self.logger.log_error(f"Error parsing OpenRouter API response: {str(e)}")
            return ""

    def _cleanup_expired_conversations(self):
        """Remove conversations inactive for more than the expiry duration"""
        now = datetime.datetime.utcnow()
        expired_users = []

        # Ideally use timestamps; here we approximate by clearing all conversations older than expiry
        # For production, store timestamps per conversation message or user.
        for user_id, messages in self.conversations.items():
            # Let's assume last message has a timestamp in assistant (not stored here),
            # so limit size for simplicity — real implementation can add timestamps.

            # For now, this function is a placeholder for future cleanup logic.
            pass

        # Remove expired conversations if any (currently none as placeholder)
        for user_id in expired_users:
            del self.conversations[user_id]
