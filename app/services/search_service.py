from app.tools.intent_classifier import classify_intent
from typing import Dict, Any
import grpc
from app.recommendations_pb2 import RecommendationRequest, RecommendationResponse
from app.recommendations_pb2_grpc import RecommendationServiceStub
from fastapi import  HTTPException
# from app.tools.memory import add_to_memory
# from agents.rlhf import refine_metadata

async def fetch_recommendations(product_id: str, user_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch personalized product recommendations via gRPC from a Go service.

    :param product_id: ID of the product for which recommendations are needed.
    :param user_metadata: Metadata containing user preferences and context.
    :return: A dictionary of recommended products.
    """
    # # Refine user metadata with RLHF
    # personalized_metadata = refine_metadata(user_metadata)

    grpc_server_address = "localhost:50051"

    async with grpc.aio.insecure_channel(grpc_server_address) as channel:
        stub = RecommendationServiceStub(channel)

        request = RecommendationRequest(
            product_id=product_id,
            user_preferences=personalized_metadata
        )

        try:
            response: RecommendationResponse = await stub.GetRecommendations(request, timeout=5.0)
            recommendations = {
                "products": [
                    {
                        "id": rec.product_id,
                        "name": rec.product_name,
                        "score": rec.relevance_score,
                    }
                    for rec in response.recommendations
                ]
            }
            return recommendations

        except grpc.RpcError as e:
            print(f"gRPC call failed: {e.details()} (Code: {e.code()})")
            raise HTTPException(status_code=500, detail="Failed to fetch recommendations.")
