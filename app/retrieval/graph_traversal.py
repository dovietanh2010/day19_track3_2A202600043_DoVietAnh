from typing import List, Dict, Any
from app.graph.neo4j_client import Neo4jClient
from app.graph.cypher_queries import CypherQueries
from app.config import Config

class GraphTraversal:
    def __init__(self):
        self.client = Neo4jClient()

    def get_subgraph(self, entity_name: str, depth: int = Config.RETRIEVAL_DEPTH) -> List[str]:
        """
        Performs BFS-like traversal to get triplets as strings.
        """
        # Using a simpler query that doesn't require APOC if possible, 
        # but the BFS path query is standard.
        cypher = """
        MATCH (n {name: $entity_name})
        MATCH path = (n)-[r*1..%d]-(m)
        RETURN path
        """ % depth
        
        results = self.client.query(cypher, {"entity_name": entity_name})
        
        triplets = set()
        for record in results:
            path = record["path"]
            for rel in path.relationships:
                start_node = rel.start_node
                end_node = rel.end_node
                rel_type = rel.type
                
                # Format: (Subject) -[RELATION]-> (Object)
                triplet_str = f"({start_node['name']}) -[{rel_type}]-> ({end_node['name']})"
                triplets.add(triplet_str)
                
        return list(triplets)
