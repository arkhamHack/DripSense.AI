from langchain.agents import initialize_agent, Tool, AgentType
from app.tools import EntityExtractionTool, QueryGeneratorTool
from app.clients import LLMClient
from app.prompts import RECOMMENDATION_PROMPT
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm_model = LLMClient.get_instance()

entity_extraction_tool = Tool(
    name="Entity Extraction",
    func=EntityExtractionTool(llm_model).run,
    description="Extracts entities like brands, attributes, and search type."
)

query_generator_tool = Tool(
    name="Cypher Query Generator",
    func=QueryGeneratorTool(llm_model).run,
    description="Generates Cypher queries based on extracted entities."
)
recommendation_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(RECOMMENDATION_SYSTEM_TEMPLATE),
    HumanMessagePromptTemplate.from_template(RECOMMENDATION_HUMAN_TEMPLATE)
])


recommendation_agent = initialize_agent(
    tools=[entity_extraction_tool, query_generator_tool],
    llm=llm_model,
    agent_type=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    agent_kwargs={
        "system_message": recommendation_prompt,
    },
    verbose=True
)
