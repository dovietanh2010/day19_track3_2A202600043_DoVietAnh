# GraphRAG with Neo4j

This project implements a complete GraphRAG (Graph Retrieval-Augmented Generation) system using Neo4j as the knowledge graph and OpenAI for extraction and generation.

## Features
- **LLM-based Extraction**: Automatically extracts entities and relationships from text.
- **Neo4j Storage**: Persists knowledge in a graph structure for multi-hop querying.
- **BFS Traversal**: Performs multi-hop retrieval to capture complex relationships.
- **Flat RAG Baseline**: Includes a vector-based RAG for comparison.
- **Evaluation**: Benchmark suite for performance and accuracy comparison.

## Setup

### 1. Prerequisites
- Python 3.10+
- Neo4j (Local or Cloud instance)
- OpenAI API Key

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

## Usage

### Ingest Data
```bash
python app/main.py --ingest
```

### Query
```bash
python app/main.py --query "Who founded OpenAI and what is their relation to Microsoft?"
```

### Compare with Flat RAG
```bash
python app/main.py --query "Who founded OpenAI?" --compare
```

### Run Benchmark
```bash
python app/evaluation/benchmark.py
```

## Project Structure
- `app/extraction`: LLM extraction logic.
- `app/graph`: Neo4j driver and builder.
- `app/retrieval`: Graph traversal and context generation.
- `app/rag`: Pipeline orchestrations.
- `app/evaluation`: Metrics and benchmarks.
