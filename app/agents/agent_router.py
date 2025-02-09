from enum import Enum
from typing import Optional
from langchain.agents import AgentExecutor

class AgentType(Enum):
    FASHION = "fashion"
    RECOMMENDATION = "recommendation"
    STYLING = "styling"  # Future agent
    OUTFIT = "outfit"    # Future agent

class AgentRouter:
    def __init__(self):
        self.agents = {}
        self._register_agents()

    def _register_agents(self):
        """Register all available agents."""
        from app.agents.fashion_assistant_agent import agent as fashion_agent
        from app.agents.recommendation_agent import recommendation_agent
        
        self.agents = {
            AgentType.FASHION: fashion_agent,
            AgentType.RECOMMENDATION: recommendation_agent,
            # Future agents can be added here
            # AgentType.STYLING: styling_agent,
            # AgentType.OUTFIT: outfit_agent,
        }

    def route_request(self, query: str, current_agent_type: AgentType) -> tuple[AgentExecutor, bool]:
        """
        Determines if request should be handled by current agent or routed to another.
        Returns (agent, should_switch)
        """
        # Add routing logic here if needed
        # For now, we'll stick with the fashion agent's built-in routing
        return self.agents[current_agent_type], False

    def get_agent(self, agent_type: AgentType) -> AgentExecutor:
        """Get agent by type."""
        return self.agents[agent_type] 