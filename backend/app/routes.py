import os

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils import handle_query
from services import fetch_recommendations
from app.agents.process_user_msg import UserMessageProcessor
from dotenv import load_dotenv
from app.agents.langchain_agent import agent

router = APIRouter()


@router.post("/more-like-this")
async def get_recommendations(product_id: str):
    """
    Accepts a product ID and returns recommendations.
    """
    recommendations = fetch_recommendations(product_id)
    return {"recommendations": recommendations}

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chatbot interactions.
    """
    await websocket.accept()
    try:
        while True:
            user_message = await websocket.receive_text()
            bot_response = agent.run(input=user_message)
            await websocket.send_text(bot_response)
    except WebSocketDisconnect:
        print("WebSocket connection closed.")
