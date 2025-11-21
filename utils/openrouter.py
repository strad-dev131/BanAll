"""
OpenRouter API Client Utility
Handles communication with OpenRouter AI models asynchronously with retries and error handling.
"""

import aiohttp
import asyncio
import json
from typing import Dict, Any
from config import Config
from utils.logger import logger


class OpenRouterClient:
    def __init__(self, config: Config):
        self.config = config
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    async def send_chat_request(self, messages: list, model: str = None) -> str:
        """Send chat messages to OpenRouter and return AI response text."""
        if model is None:
            model = self.config.CHATBOT_MODEL

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://github.com/strad-dev131/BanAll",  # Optional but recommended
            "X-Title": "BanAll ChatBot"  # Optional but recommended
        }

        payload = {
            "model": model,
            "messages": messages
        }

        # Debug logging
        logger.log_action("OPENROUTER_REQUEST", 0, 0, {
            "model": model,
            "message_count": len(messages),
            "api_key_present": bool(self.config.OPENROUTER_API_KEY),
            "api_key_length": len(self.config.OPENROUTER_API_KEY) if self.config.OPENROUTER_API_KEY else 0
        })

        for attempt in range(1, self.max_retries + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        self.api_url, 
                        json=payload, 
                        headers=headers, 
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as resp:
                        response_text = await resp.text()
                        
                        if resp.status == 200:
                            try:
                                data = json.loads(response_text)
                                reply = self._extract_response(data)
                                if reply:
                                    logger.log_action("OPENROUTER_API_SUCCESS", 0, 0, {
                                        "attempt": attempt,
                                        "response_length": len(reply)
                                    })
                                    return reply
                                else:
                                    logger.log_error(f"Empty response from OpenRouter API. Full response: {response_text[:500]}")
                            except json.JSONDecodeError as je:
                                logger.log_error(f"JSON decode error: {je}. Response: {response_text[:500]}")
                        else:
                            logger.log_error(
                                f"OpenRouter API HTTP {resp.status}: {response_text[:500]}",
                                f"Attempt {attempt}/{self.max_retries}"
                            )

            except aiohttp.ClientError as e:
                logger.log_error(f"OpenRouter API client error on attempt {attempt}: {str(e)}")
            except asyncio.TimeoutError:
                logger.log_error(f"OpenRouter API timeout on attempt {attempt}")
            except Exception as e:
                logger.log_error(f"Unexpected error during OpenRouter API call: {str(e)}")

            if attempt < self.max_retries:
                await asyncio.sleep(self.retry_delay * attempt)  # Exponential backoff

        # After retries failed
        logger.log_error(f"OpenRouter API failed after {self.max_retries} attempts.")
        return ""

    def _extract_response(self, response_json: Dict[str, Any]) -> str:
        """
        Extract assistant text from OpenRouter API response.
        Handles possible response formats gracefully.
        """
        try:
            choices = response_json.get("choices", [])
            if choices and isinstance(choices, list):
                message_obj = choices[0].get("message", {})
                content = message_obj.get("content", "")
                return content.strip()
            return ""
        except Exception as e:
            logger.log_error(f"Error parsing OpenRouter API response: {str(e)}")
            return ""
