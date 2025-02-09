from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import MessagesPlaceholder
from langchain.tools import tool
from app.clients import LLMClient
from app.tools import IntentTool ,MemoryTool
from app.prompts import AGENT_PROMPT,SYSTEM_PROMPT
from app.agents.recommendation_agent import recommendation_agent
import json

# processor = UserMessageProcessor(llm_model, grpc_server_address=f"{grpc_host}:{grpc_port}")

llm_model = LLMClient.get_instance()

@tool
def classify_intent_tool(user_message: str) -> str:
    """
    A LangChain tool to classify user intent.
    """
    intent_tool = IntentTool(llm_model=llm_model)
    return intent_tool.classify_intent(user_message)


@tool
def get_product_recommendations(query: str) -> str:
    """Delegates product recommendation requests to the specialized recommendation agent."""
    try:
        response = recommendation_agent.run(query)
        return response
    except Exception as e:
        return f"Error getting recommendations: {str(e)}"

    
@tool
def analyze_chat_history(query: str) -> str:
    """Analyzes chat history with chain-of-thought reasoning."""
    memory_tool = MemoryTool()
    context = memory_tool.search_context(query)
    
    analysis_prompt = f"""
    Analyze the following chat history and user query using these steps:
    1. Identify previously mentioned products
    2. Filter products based on the current query criteria
    3. Compare and rank suitable products
    4. Explain reasoning for recommendations

    User Query: {query}
    Chat Context: {json.dumps(context, indent=2)}
    """
    return llm_model.analyze(analysis_prompt)

tools = [
    Tool(
        name="Classify Intent",
        func=classify_intent_tool,
        description="ALWAYS use this first to determine if the query needs fashion advice, chat history, or product recommendations."
    ),
    Tool(
        name="Analyze Chat History",
        func=analyze_chat_history,
        description="Use when user refers to previous products or conversations."
    ),
    Tool(
        name="Get Product Recommendations",
        func=get_product_recommendations,
        description="Use when user wants product recommendations. This will engage the specialized recommendation agent."
    )
]

agent = initialize_agent(
    tools,
    llm_model,
    agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    agent_kwargs={
        "system_message": SYSTEM_PROMPT,
        "memory_prompts": [MessagesPlaceholder(variable_name="conversation")],
    },
    handle_parsing_errors=True,
    verbose=True
)
