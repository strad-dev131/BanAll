"""
OpenRouter API Client Utility - Production Grade
Handles communication with OpenRouter AI models with full debugging
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
        self.max_retries = 2
        self.retry_delay = 1

    async def send_chat_request(self, messages: list, model: str = None) -> str:
        """Send chat messages to OpenRouter and return AI response text."""
        if model is None:
            model = self.config.CHATBOT_MODEL

        # Validate API key
        if not self.config.OPENROUTER_API_KEY:
            logger.log_error("OPENROUTER_API_KEY is missing or empty!")
            return ""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://github.com/strad-dev131/BanAll",
            "X-Title": "BanAll ChatBot"
        }

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 150,  # Keep responses concise
            "temperature": 0.7   # Natural conversation
        }

        # Debug: Log request details
        logger.log_action("OPENROUTER_REQUEST_START", 0, 0, {
            "model": model,
            "messages_count": len(messages),
            "last_user_message": messages[-1].get("content", "")[:50] if messages else "none"
        })

        for attempt in range(1, self.max_retries + 1):
            try:
                timeout = aiohttp.ClientTimeout(total=20)
                
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    logger.log_action("OPENROUTER_ATTEMPT", 0, 0, {"attempt": attempt})
                    
                    async with session.post(self.api_url, json=payload, headers=headers) as resp:
                        status_code = resp.status
                        response_text = await resp.text()
                        
                        logger.log_action("OPENROUTER_RESPONSE_RECEIVED", 0, 0, {
                            "status": status_code,
                            "response_preview": response_text[:200]
                        })
                        
                        if status_code == 200:
                            try:
                                data = json.loads(response_text)
                                reply = self._extract_response(data)
                                
                                if reply:
                                    logger.log_action("OPENROUTER_SUCCESS", 0, 0, {
                                        "reply_length": len(reply),
                                        "reply_preview": reply[:100]
                                    })
                                    return reply
                                else:
                                    logger.log_error(f"Empty content in response. Full JSON: {json.dumps(data, indent=2)[:500]}")
                                    
                            except json.JSONDecodeError as je:
                                logger.log_error(f"JSON decode failed: {str(je)}. Raw response: {response_text[:300]}")
                        else:
                            logger.log_error(f"HTTP {status_code} error. Response: {response_text[:500]}")

            except asyncio.TimeoutError:
                logger.log_error(f"Request timeout on attempt {attempt}")
            except aiohttp.ClientError as e:
                logger.log_error(f"Network error on attempt {attempt}: {type(e).__name__} - {str(e)}")
            except Exception as e:
                logger.log_error(f"Unexpected error on attempt {attempt}: {type(e).__name__} - {str(e)}")

            if attempt < self.max_retries:
                await asyncio.sleep(self.retry_delay)

        logger.log_error(f"All {self.max_retries} attempts failed")
        return ""

    def _extract_response(self, response_json: Dict[str, Any]) -> str:
        """Extract assistant text from OpenRouter API response"""
        try:
            # Log the structure for debugging
            logger.log_action("PARSING_RESPONSE", 0, 0, {
                "has_choices": "choices" in response_json,
                "choices_type": type(response_json.get("choices")).__name__ if "choices" in response_json else "missing"
            })
            
            choices = response_json.get("choices", [])
            if not choices or not isinstance(choices, list):
                logger.log_error(f"Invalid choices format. Response keys: {list(response_json.keys())}")
                return ""
            
            if len(choices) == 0:
                logger.log_error("Choices array is empty")
                return ""
            
            message_obj = choices[0].get("message", {})
            content = message_obj.get("content", "")
            
            if not content:
                logger.log_error(f"Content is empty. Message object: {json.dumps(message_obj, indent=2)}")
            
            return content.strip()
            
        except Exception as e:
            logger.log_error(f"Response parsing error: {type(e).__name__} - {str(e)}")
            return ""
