from typing import List, Dict

class QueryExample:
    def __init__(
        self,
        user_query: str,
        entities: Dict,
        search_type: str,
        cypher_query: str
    ):
        self.user_query = user_query
        self.entities = entities
        self.search_type = search_type
        self.cypher_query = cypher_query

def create_training_dataset() -> List[Dict]:
    return [
        {
            "input": """Schema:
Nodes: {
    Product: [id, name, brand, color, price, category],
    Brand: [id, name, tier],
    Category: [id, name, parent_category]
}
Relationships: {
    BELONGS_TO: [Product->Category],
    MADE_BY: [Product->Brand],
    SIMILAR_TO: [Product->Product, similarity_score],
    COMPLEMENTS: [Product->Product, confidence]
}
Indexes: {
    Product: [name, color, price],
    Brand: [name],
    Category: [name]
}

User Query: "Show me blue dresses under $100"
Entities: {
    "color": "blue",
    "category": "dress",
    "price_range": "<100"
}""",
            "output": """MATCH (p:Product)-[:BELONGS_TO]->(c:Category)
WHERE c.name =~ '(?i).*dress.*'
  AND p.color =~ '(?i).*blue.*'
  AND p.price < 100
RETURN p.name, p.brand, p.price, p.color
ORDER BY p.price ASC
LIMIT 10"""
        },
        # Add more examples...
    ]