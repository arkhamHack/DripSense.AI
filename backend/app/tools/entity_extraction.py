from langchain.tools import BaseTool

class EntityExtractionTool(BaseTool):
    def __init__(self, llm):
        self.llm = llm

    def _run(self, query):
        prompt = f"""
        Analyze the query and extract entities in a structured JSON format. Entities include:
        -Brand
        -Attribute
        -Color
        -Price
        Ensure that:
        - Attributes are a list of dictionaries, where each dictionary has "key" and "value" pairs.
        - Brands are a list of strings.
        - Colors are a list of strings.
        - Price are a list of strings as well.
        - The search type is one of "vector", "full-text", or "hybrid".
        - Only include entities explicitly mentioned in the query. If an entity type is missing, omit it from the JSON. 
        Also keep the original query as a part of the json with a field called query. 

        Example Output:
        {{
            "brands": ["Zara"],
            "attributes": [
                {{"key": "color", "value": "red"}},
                {{"key": "category", "value": "dress"}},
                 {{"key": "body_shape", "value": "M"}}
            ],
            "search_type": "vector"
        }}

        Query: "{query}"
        JSON Response:
        """
        response = self.llm.generate(prompt)
        return response