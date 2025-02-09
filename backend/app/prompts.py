from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

followup_prompt = PromptTemplate(
    input_variables=["history", "current_question", "metadata"],
    template="""
You are a fashion assistant. Use the conversation history and product metadata to answer the user's question.

Conversation History:
{history}

Product Metadata:
{metadata}

Current User Question: {current_question}

Assistant Answer:
"""
)

qa_prompt = PromptTemplate(
    input_variables=["user_message"],
    template="""
You are a friendly and knowledgeable fashion assistant chatbot. Respond to general questions about fashion trends, the business, and greetings. Provide concise and helpful responses.

User Message: {user_message}

Assistant Response:
"""
)


intent_prompt = PromptTemplate(
    input_variables=["message"],
    template="""
You are a fashion assistant. Classify the user's intent from the following categories:
- QA: Direct question about a product, brand, or attribute.
- Follow-up: Builds on the previous conversation.
- Recommendation: Suggests products based on preferences.

Message: "{message}"
Classify the intent:""")

class FinalResponse(BaseModel):
    helpful: bool = Field(description="Whether the answer is helpful and informative.")
    final_answer: str = Field(description="The final answer to the user's query.")


def parse_response(raw_response: str) -> FinalResponse:
    return FinalResponse.parse_obj(
        llm(f"""
        Analyze the following response and classify if it is helpful or requires additional information:

        Response: {raw_response}

        Provide a JSON with "helpful" and "final_answer".
        """)
    )


class ContextQueryResponse(BaseModel):
    relevant: bool = Field(description="Whether the chat history in context is relevant to the user query.")
    query: str = Field(description="The final query, taking into account the chat history context.")

from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import MessagesPlaceholder, PromptTemplate
from langchain.tools import tool
from app.clients import LLMClient
from app.tools import IntentTool, MemoryTool, QueryGeneratorTool

llm_model = LLMClient.get_instance()

@tool
def classify_intent_tool(user_message: str) -> str:
    """Classifies if the query is a general fashion question, requires chat history, 
    or needs product recommendations."""
    intent_tool = IntentTool(llm_model=llm_model)
    return intent_tool.classify_intent(user_message)

@tool
def query_chat_history_tool(query: str) -> str:
    """Searches through previous conversation history for relevant context."""
    memory_tool = MemoryTool()
    return memory_tool.search_messages(query)

@tool
def query_generator_tool(search_criteria: str) -> str:
    """Generates Cypher query for product search based on user criteria."""
    query_tool = QueryGeneratorTool(llm_model=llm_model)
    return query_tool.generate_query(search_criteria)

# Define tools with clear purposes
tools = [
    Tool(
        name="Classify Intent",
        func=classify_intent_tool,
        description="Use this first to determine if the query needs fashion advice, chat history, or product recommendations."
    ),
    Tool(
        name="Search Chat History",
        func=query_chat_history_tool,
        description="Search previous conversations when user refers to past interactions."
    ),
    Tool(
        name="Generate Product Query",
        func=query_generator_tool,
        description="Generate search query when user wants product recommendations."
    )
]

# Custom prompt to guide the agent's decision-making
AGENT_PROMPT = PromptTemplate.from_template("""
You are a fashion assistant. First, classify the user's intent to determine the appropriate response:
1. For general fashion advice, respond directly
2. If the query references previous conversations, use the chat history tool
3. For product recommendations, use the query generator tool

Current conversation:
{conversation}""")

SYSTEM_PROMPT = """You are a fashion assistant that coordinates between different specialized tools.
Follow this decision flow:

1. ALWAYS start with "Classify Intent" to categorize the query as:
   - General fashion advice
   - Reference to previous conversations
   - Product recommendation request
   - Hybrid (combining multiple types)

2. Based on the intent:
   A. For general fashion advice: Respond directly
   B. For previous conversation references: Use "Analyze Chat History"
   C. For product recommendations: Use "Get Product Recommendations"
   D. For hybrid queries:
      - First use "Analyze Chat History" to understand context
      - Then use "Get Product Recommendations" with the enhanced context

Examples:
- "What goes well with jeans?" -> Direct fashion advice
- "Quickly show me the black kurtis which you " -> Analyze Chat History
- "Show me blue dresses" -> Get Product Recommendations
- "Show me dresses similar to the red one earlier but in blue" -> Analyze Chat History + Get Product Recommendations

Always explain your reasoning before using each tool.
"""
RECOMMENDATION_HUMAN_TEMPLATE = "{input}"
RECOMMENDATION_SYSTEM_TEMPLATE = """You are a specialized fashion recommendation engine.
Your task is to understand product requirements and generate accurate search queries.

For the following user request:
{input}

Follow these steps:
1. Extract key product attributes (color, style, occasion, etc.)
2. Identify any brand preferences
3. Note price range if mentioned
4. Generate appropriate search query

Consider multilingual fashion terms:
- Traditional: kurta, saree, lehenga
- Western: dress, jeans, tops
- Attributes in Hinglish: "thoda loose", "fitted wala"
"""

