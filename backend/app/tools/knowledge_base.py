class KnowledgeBase:
    def __init__(self, schema):
        self.schema = schema

    def get_node_types(self):
        return list(self.schema.keys())

    def get_relations(self, node_type):
        return self.schema.get(node_type, {}).get("relations", [])

# Example schema
SCHEMA = {
    "Product": {
        "relation": {
            "relations_from":["HAS_BRAND", "HAS_ATTRIBUTE", "HAS_COLOR", "HAS_PRICE"]
        }
    },
    "Brand": {
        "relations": {
            "relations_from":[],
            "relations_to":["HAS_BRAND"]
        }
    },
    "Attribute": {
        "relations": {
            "relations_from":[],
            "relations_to":["HAS_ATTRIBUTE"]
        }
    },
    "Color": {
        "relations": {
            "relations_from":[],
            "relations_to":["HAS_COLOR"]
        }
    },
    "Price": {
        "relations": []
    }
}

knowledge_base = KnowledgeBase(SCHEMA)
