from app.extraction.entity_extractor import EntityExtractor
from app.graph.graph_builder import GraphBuilder
from app.retrieval.query_engine import QueryEngine
from app.utils.logger import setup_logger

logger = setup_logger("GraphRAG")

class GraphRAGPipeline:
    def __init__(self, corpus_path: str):
        self.corpus_path = corpus_path
        self.extractor = EntityExtractor()
        self.builder = GraphBuilder()
        self.query_engine = QueryEngine()

    def ingest(self):
        logger.info("Starting ingestion...")
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Ingest in chunks
        for line in lines:
            if not line.strip():
                continue
            logger.info(f"Extracting from: {line[:50]}...")
            res = self.extractor.extract(line)
            self.builder.build_graph(res.entities, res.triplets)
            
        logger.info("Ingestion complete.")

    def search(self, query: str) -> str:
        return self.query_engine.query(query)
