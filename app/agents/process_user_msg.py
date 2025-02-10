from typing import Dict, Any
from app.tools import IntentTool, MemoryTool,QueryGeneratorTool


class UserMessageProcessor:
    def __init__(self, grpc_server_address: str = "localhost:50051"):
        self.intent_tool = IntentTool()
        self.query_tool = QueryGeneratorTool(grpc_server_address)
        self.memory_tool = MemoryTool()

    async def process(self, user_message: str, metadata: Dict[str, Any]) -> str:
        """
        Process the user's message, classify the intent, and respond accordingly.

        :param user_message: User's message.
        :param metadata: Context metadata.
        :return: Bot's response.
        """
        intent = self.intent_tool.classify(user_message)

        if intent == "QA":
            response = self.handle_qa_intent(user_message)
        elif intent == "Follow-up":
            response = self.handle_followup_intent(user_message, metadata)
        elif intent == "Recsys":
            response = await self.handle_recsys_intent(metadata)
        else:
            response = "As a fashion assistant, I am unable to understand you."

        # Store the conversation in memory
        self.memory_tool.store_message(user_message, response)
        return response

    async def handle_recsys_intent(self, metadata: Dict[str, Any]) -> str:
        product_id = metadata.get("product_id")
        user_metadata = metadata.get("user_metadata", {})
        recommendations = await self.query_tool.fetch_recommendations(product_id, user_metadata)
        return f"Here are some recommendations: {recommendations}"
