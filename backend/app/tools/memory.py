from langchain.memory import ConversationBufferMemory
from typing import List, Tuple, Optional
from app.clients import RedisClient
from datetime import datetime
import json
memory = ConversationBufferMemory()
redis_client = RedisClient.get_instance()

class MemoryTool:
    @staticmethod
    def store_message(user_message: str, bot_response: str) -> None:
        """Store a message-response pair with timestamp and parsed product info."""
        timestamp = datetime.now().isoformat()
        
        # Extract product information if present in bot response
        products_mentioned = MemoryTool._extract_products(bot_response)
        
        message_data = {
            "timestamp": timestamp,
            "user_message": user_message,
            "bot_response": bot_response,
            "products": products_mentioned
        }
        
        redis_client.rpush(MEMORY_KEY, json.dumps(message_data))

    @staticmethod
    def _extract_products(response: str) -> List[dict]:
        """Helper method to parse product information from responses."""
        # This is a simplified example - you might want to use regex or LLM to extract product details
        # Returns list of products with their attributes
        return []

    @staticmethod
    def search_context(query: str, limit: int = 5) -> dict:
        """
        Smart context retrieval with product focus.
        Returns relevant messages and extracted product information.
        """
        all_messages = redis_client.lrange(MEMORY_KEY, -20, -1)  # Get last 20 messages
        relevant_context = {
            "messages": [],
            "products": [],
            "summary": ""
        }
        
        for msg_str in all_messages:
            msg_data = json.loads(msg_str)
            # Add messages to context if they contain product information
            if msg_data["products"]:
                relevant_context["products"].extend(msg_data["products"])
            relevant_context["messages"].append({
                "timestamp": msg_data["timestamp"],
                "exchange": (msg_data["user_message"], msg_data["bot_response"])
            })
        
        return relevant_context