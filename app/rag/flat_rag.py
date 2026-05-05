import numpy as np
import faiss
from typing import List
from openai import OpenAI
from app.config import Config

class FlatRAG:
    def __init__(self, corpus_path: str):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.corpus_path = corpus_path
        self.chunks = self._load_and_chunk()
        self.index_flat = None

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
        embeddings = []
        for chunk in self.chunks:
            embeddings.append(self._get_embedding(chunk))
        
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Normalize vectors for cosine similarity (using IndexFlatIP)
        faiss.normalize_L2(embeddings_array)
        
        dimension = embeddings_array.shape[1]
        self.index_flat = faiss.IndexFlatIP(dimension)
        self.index_flat.add(embeddings_array)

    def retrieve(self, query: str, k: int = Config.TOP_K) -> List[str]:
        if self.index_flat is None:
            raise ValueError("Index not initialized. Call index() first.")
            
        query_embedding = np.array([self._get_embedding(query)]).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search in FAISS index
        scores, indices = self.index_flat.search(query_embedding, k)
        
        return [self.chunks[i] for i in indices[0] if i != -1]

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
