from typing import List
from app.graph.neo4j_client import Neo4jClient
from app.extraction.schema import Triplet, Entity
from app.utils.logger import setup_logger

logger = setup_logger("GraphBuilder")

class GraphBuilder:
    def __init__(self):
        self.client = Neo4jClient()

    def build_graph(self, entities: List[Entity], triplets: List[Triplet]):
        # 1. Create Nodes
        for entity in entities:
            cypher = f"MERGE (n:{entity.type} {{name: $name}})"
            self.client.execute_write(cypher, {"name": entity.name})
        
        # 2. Create Relationships
        for triplet in triplets:
            # Use dynamic labels for nodes if available, otherwise default to Entity
            sub_label = triplet.subject_type if triplet.subject_type else "Entity"
            obj_label = triplet.object_type if triplet.object_type else "Entity"
            
            cypher = (
                f"MERGE (s:{sub_label} {{name: $sub_name}}) "
                f"MERGE (o:{obj_label} {{name: $obj_name}}) "
                f"MERGE (s)-[r:{triplet.relation}]->(o)"
            )
            self.client.execute_write(cypher, {
                "sub_name": triplet.subject,
                "obj_name": triplet.object
            })
            
        logger.info(f"Successfully processed {len(entities)} entities and {len(triplets)} triplets.")

    def clear_database(self):
        self.client.execute_write("MATCH (n) DETACH DELETE n")
        logger.info("Database cleared.")
