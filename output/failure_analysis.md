# Failure Modes Analysis Report

## 1. Kiến thức ngoài & Nguy cơ Ảo giác (Flat RAG)
Đây là các trường hợp Flat RAG tự ý sử dụng kiến thức bên ngoài, vi phạm nguyên tắc 'Groundedness' của RAG:

### Query: How much did Microsoft invest in OpenAI in 2019?
- **Flat RAG (Hallucination/Leakage)**: Microsoft invested $1 billion in OpenAI in 2019.
- **GraphRAG (Grounded)**: The provided context does not specify the amount Microsoft invested in OpenAI in 2019. Therefore, I don't know.
- **Phân tích**: Thông tin này không có trong tài liệu nạp vào. GraphRAG tuân thủ đúng dữ liệu, Flat RAG tự bổ sung kiến thức ngoài.

### Query: Which GPUs power modern LLM training?
- **Flat RAG (Hallucination/Leakage)**: The GPUs that power most modern LLM training are the H100 GPUs provided by NVIDIA.
- **GraphRAG (Grounded)**: I don't know.
- **Phân tích**: Thông tin này không có trong tài liệu nạp vào. GraphRAG tuân thủ đúng dữ liệu, Flat RAG tự bổ sung kiến thức ngoài.

### Query: Is Llama open-source?
- **Flat RAG (Hallucination/Leakage)**: Yes, Llama is open-source.
- **GraphRAG (Grounded)**: I don't know.
- **Phân tích**: Thông tin này không có trong tài liệu nạp vào. GraphRAG tuân thủ đúng dữ liệu, Flat RAG tự bổ sung kiến thức ngoài.

## 2. Thành công của Truy vấn Đa bước (GraphRAG)
Các trường hợp GraphRAG kết nối thực thể tốt hơn:

- **Câu hỏi**: Who founded OpenAI?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: When was DeepMind acquired and by whom?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: Who is the CEO of NVIDIA?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: What organization does Mustafa Suleyman lead now?
  - GraphRAG: 3đ | Flat RAG: 3đ
- **Câu hỏi**: Who founded Anthropic and where did they work before?
  - GraphRAG: 9đ | Flat RAG: 8đ
- **Câu hỏi**: What model did Google launch to compete with GPT-4?
  - GraphRAG: 9đ | Flat RAG: 8đ
- **Câu hỏi**: Who is the CEO of Apple?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: What is the relationship between Sam Altman and Microsoft?
  - GraphRAG: 10đ | Flat RAG: 9đ
- **Câu hỏi**: Who are the founders of DeepMind?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: When was ChatGPT released?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: What did Amazon invest in Anthropic for?
  - GraphRAG: 8đ | Flat RAG: 8đ
- **Câu hỏi**: Who is the CEO of Alphabet?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: When was OpenAI founded?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: What organization did Satya Nadella lead in 2014?
  - GraphRAG: 10đ | Flat RAG: 10đ
- **Câu hỏi**: What is Apple Intelligence?
  - GraphRAG: 5đ | Flat RAG: 2đ
