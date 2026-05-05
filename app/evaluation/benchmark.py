import time
import os
import sys
import pandas as pd

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.rag.graphrag import GraphRAGPipeline
from app.rag.flat_rag import FlatRAG
from app.evaluation.metrics import Metrics

def run_benchmark():
    corpus_path = os.path.join("data", "tech_company_corpus.txt")
    report_dir = os.path.join("output")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    queries = [
        "Who founded OpenAI?",
        "When was DeepMind acquired and by whom?",
        "Who is the CEO of NVIDIA?",
        "What organization does Mustafa Suleyman lead now?",
        "Who founded Anthropic and where did they work before?",
        "What model did Google launch to compete with GPT-4?",
        "How much did Microsoft invest in OpenAI in 2019?",
        "Who is the CEO of Apple?",
        "What is the relationship between Sam Altman and Microsoft?",
        "Who are the founders of DeepMind?",
        "When was ChatGPT released?",
        "What did Amazon invest in Anthropic for?",
        "Who leads Tesla and xAI?",
        "What is the connection between Mistral AI and Meta?",
        "Who is the CEO of Alphabet?",
        "When was OpenAI founded?",
        "What organization did Satya Nadella lead in 2014?",
        "What is Apple Intelligence?",
        "Which GPUs power modern LLM training?",
        "Is Llama open-source?"
    ]
    
    pipeline = GraphRAGPipeline(corpus_path)
    flat_rag = FlatRAG(corpus_path)
    metrics = Metrics()
    
    print("Indexing Flat RAG...")
    flat_rag.index()
    
    results = []
    
    print("\nStarting Benchmark with Accuracy Scoring...\n")
    
    for q in queries:
        print(f"Processing query: {q}")
        # GraphRAG
        start = time.time()
        g_res = pipeline.search(q)
        g_time = time.time() - start
        g_score, g_reason = metrics.score_accuracy(q, g_res['answer'])
        
        # Flat RAG
        start = time.time()
        f_res = flat_rag.query(q)
        f_time = time.time() - start
        f_score, f_reason = metrics.score_accuracy(q, f_res['answer'])
        
        results.append({
            "Query": q,
            "GRAG_Time": g_time,
            "GRAG_Tokens": g_res['tokens'],
            "GRAG_Score": g_score,
            "GRAG_Answer": g_res['answer'],
            "FRAG_Time": f_time,
            "FRAG_Tokens": f_res['tokens'],
            "FRAG_Score": f_score,
            "FRAG_Answer": f_res['answer']
        })

    # Save to CSV
    df = pd.DataFrame(results)
    csv_path = os.path.join(report_dir, "benchmark_results.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nResults saved to {csv_path}")
    
if __name__ == "__main__":
    run_benchmark()
