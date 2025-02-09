from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional
from app.prompts import intent_prompt

class IntentTool:
    def __init__(self, llm_model):
        self.llm = llm_model

    def classify_intent(self,message: str) -> str:
        """
        Classify the intent of a user message using Gemini

        Args:
            message: User's input message

        Returns:
            Classified intent as string
        """
        if self.llm is None:
            raise ValueError("LLM not initialized. Please call setup_gemini first.")

        response = self.llm.invoke(intent_prompt.format(message=message))
        return response.content.strip()

