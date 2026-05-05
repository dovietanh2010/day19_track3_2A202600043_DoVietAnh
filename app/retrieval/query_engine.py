import json
from typing import List
from openai import OpenAI
from app.config import Config
from app.retrieval.graph_traversal import GraphTraversal
from app.retrieval.text_generator import TextGenerator
from app.graph.neo4j_client import Neo4jClient
from app.graph.cypher_queries import CypherQueries

class QueryEngine:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.traversal = GraphTraversal()
        self.neo4j = Neo4jClient()

    def extract_keywords(self, query: str) -> List[str]:
        """
        Extract key entities from the user query using LLM.
        """
        prompt = f"Extract the main entities (companies, people, years) from this query as a JSON list of strings: '{query}'"
        
        response = self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        try:
            content = json.loads(response.choices[0].message.content)
            # Find the list in the JSON
            for key in content:
                if isinstance(content[key], list):
                    return content[key]
            return []
        except:
            return []

    def find_matching_nodes(self, keywords: List[str]) -> List[str]:
        """
        Matches keywords to actual node names in Neo4j.
        """
        matched_names = []
        for kw in keywords:
            # Case-insensitive regex match
            results = self.neo4j.query(
                CypherQueries.FIND_ENTITY, 
                {"regex": f"(?i).*{kw}.*"}
            )
            for res in results:
                matched_names.append(res["name"])
        return list(set(matched_names))

    def query(self, user_query: str) -> dict:
        # 1. Extract keywords
        keywords = self.extract_keywords(user_query)
        
        # 2. Match to graph nodes
        node_names = self.find_matching_nodes(keywords)
        
        # 3. Traversal
        all_triplets = []
        for name in node_names:
            all_triplets.extend(self.traversal.get_subgraph(name))
        
        # 4. Generate context
        graph_context = TextGenerator.subgraph_to_context(list(set(all_triplets)))
        
        # 5. Final LLM Answer
        final_prompt = TextGenerator.generate_final_prompt(user_query, graph_context)
        
        response = self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": final_prompt}]
        )
        
        return {
            "answer": response.choices[0].message.content,
            "tokens": response.usage.total_tokens
        }
