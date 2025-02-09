from langchain.tools import BaseTool
from typing import Dict, List, Optional
from pydantic import BaseModel
import vertexai
from vertexai.language_models import TextGenerationModel
import torch
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer

class QuerySchema(BaseModel):
    """Schema for Neo4j database"""
    model_config = {
        "json_schema_extra": {
            "nodes": Dict[str, List[str]],  # node_type: [properties]
            "relationships": Dict[str, List[str]],  # relationship_type: [properties]
            "indexes": Dict[str, List[str]]  # node_type: [indexed_properties]
        }
    }
    nodes: Dict[str, List[str]]
    relationships: Dict[str, List[str]]
    indexes: Dict[str, List[str]]

class QueryGeneratorTool(BaseTool):
    name = "cypher_query_generator"
    description = "Generates Cypher queries for Neo4j based on natural language input"

    def __init__(self, model_path: str, schema: QuerySchema):
        super().__init__()
        self.model_json_schema = schema
        self.model = self._load_model(model_path)
        
    def _load_model(self, model_path: str):
        """Load the fine-tuned model"""
        base_model = TextGenerationModel.from_pretrained("text-bison@001")
        # Add PEFT/LoRA configuration here
        return base_model

    def _format_prompt(self, query: str, entities: Dict) -> str:
        """Format prompt with schema and extracted entities"""
        return f"""Given the following database schema:
Nodes: {self.model_json_schema.nodes}
Relationships: {self.model_json_schema.relationships}
Indexes: {self.model_json_schema.indexes}

And these extracted entities:
{entities}

Generate a Cypher query for this request: {query}

Consider these search types:
1. Basic product search
2. Similar product search
3. Complementary product search
4. Outfit-based search
5. Trend-based search

The query should:
- Use appropriate indexes
- Include relevant relationships
- Handle multiple filtering conditions
- Return required properties

Generate Cypher query:"""

    def _run(self, query: str, entities: Dict) -> str:
        """Generate Cypher query based on input"""
        prompt = self._format_prompt(query, entities)
        response = self.model.predict(prompt)
        return response.text
