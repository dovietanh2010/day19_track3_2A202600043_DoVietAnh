import argparse
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.graphrag import GraphRAGPipeline
from app.rag.flat_rag import FlatRAG
from app.config import Config

def main():
    parser = argparse.ArgumentParser(description="GraphRAG with Neo4j")
    parser.add_argument("--query", type=str, help="Query the GraphRAG system")
    parser.add_argument("--ingest", action="store_true", help="Ingest the corpus into Neo4j")
    parser.add_argument("--compare", action="store_true", help="Compare with Flat RAG")
    
    args = parser.parse_args()
    
    corpus_path = os.path.join("data", "tech_company_corpus.txt")
    pipeline = GraphRAGPipeline(corpus_path)
    
    if args.ingest:
        pipeline.ingest()
        print("Ingestion complete.")
        
    if args.query:
        result = pipeline.search(args.query)
        print(f"\nGraphRAG Answer:\n{result['answer']}")
        
    if args.compare and args.query:
        flat_rag = FlatRAG(corpus_path)
        print("\nIndexing Flat RAG (this may take a moment)...")
        flat_rag.index()
        flat_result = flat_rag.query(args.query)
        print(f"\nFlat RAG Answer:\n{flat_result['answer']}")

if __name__ == "__main__":
    main()
