from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


class EmbeddingClient:
    _instance = None

    @classmethod
    def initialize(cls, model_name: str):
        if cls._instance is None:
            genai.configure(api_key=api_key)
            cls._instance = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0,
                convert_system_message_to_human=True,
                top_p=0.1,
            )
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("EmbeddingClient not initialized. Call LLMClient.initialize() first.")
        return cls._instance
