import numpy as np
from typing import List
from openai import OpenAI
from app.config import Config

class FlatRAG:
    def __init__(self, corpus_path: str):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.corpus_path = corpus_path
        self.chunks = self._load_and_chunk()
        self.embeddings = []

    def _load_and_chunk(self) -> List[str]:
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            text = f.read()
        # Simple line-based chunking for demonstration
        return [line.strip() for line in text.split("\n") if line.strip()]

    def _get_embedding(self, text: str):
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def index(self):
        for chunk in self.chunks:
            self.embeddings.append(self._get_embedding(chunk))
        self.embeddings = np.array(self.embeddings)

    def retrieve(self, query: str, k: int = Config.TOP_K) -> List[str]:
        query_embedding = self._get_embedding(query)
        # Cosine similarity
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        top_indices = np.argsort(similarities)[-k:][::-1]
        return [self.chunks[i] for i in top_indices]

    def query(self, user_query: str) -> dict:
        relevant_chunks = self.retrieve(user_query)
        context = "\n".join(relevant_chunks)
        
        prompt = f"""
        Answer the question based on the text context below.
        
        Question: {user_query}
        
        Context:
        {context}
        """
        
        response = self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "answer": response.choices[0].message.content,
            "tokens": response.usage.total_tokens
        }
