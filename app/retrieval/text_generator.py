from typing import List

class TextGenerator:
    @staticmethod
    def subgraph_to_context(triplets: List[str]) -> str:
        if not triplets:
            return "No relevant graph data found."
            
        context = "The following relationships were found in the knowledge graph:\n"
        for triplet in triplets:
            context += f"- {triplet}\n"
        return context

    @staticmethod
    def generate_final_prompt(query: str, graph_context: str, flat_context: str = "") -> str:
        prompt = f"""
        Answer the user's question based on the provided context.
        
        Question: {query}
        
        Graph Context:
        {graph_context}
        
        Additional Text Context:
        {flat_context}
        
        If the information is not in the context, say you don't know.
        """
        return prompt
