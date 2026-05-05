# BÁO CÁO DỰ ÁN GRAPHRAG (TECH COMPANY CORPUS)

## 1. Mã nguồn (Source Code)
Toàn bộ mã nguồn được tổ chức theo cấu trúc module chuyên nghiệp:
- `app/extraction/`: Trích xuất thực thể và quan hệ (LLM-based).
- `app/graph/`: Quản lý kết nối và truy vấn Neo4j.
- `app/retrieval/`: Logic duyệt đồ thị 2-hop và tổng hợp câu trả lời.
- `app/rag/`: Triển khai Pipeline GraphRAG và Flat RAG (Baseline).
- `app/evaluation/`: Hệ thống chấm điểm tự động (LLM Judge) và Benchmark.

## 2. Đồ thị tri thức (Knowledge Graph)
Đồ thị được xây dựng trên Neo4j Desktop với các thực thể (Organization, Person, Product, Technology) và các mối quan hệ (FOUNDED_BY, INVESTED_IN, CEO_OF, DEVELOPED, v.v.).

![Knowledge Graph Visualization](output/visualization.svg)

## 3. Bảng so sánh kết quả 20 câu hỏi Benchmark
Dưới đây là tóm tắt kết quả so sánh giữa Flat RAG và GraphRAG:

| Chỉ số | GraphRAG (Trung bình) | Flat RAG (Trung bình) |
|--------|-----------------------|-----------------------|
| **Accuracy Score (0-10)** | 8.10 | 8.45 |
| **Latency (Seconds)** | ~2.5s | ~1.5s |
| **Token Usage** | ~420 tokens | ~180 tokens |

*(Chi tiết từng câu hỏi có trong file output/benchmark_results.csv)*

Nhận xét:
 - Flat RAG có độ chính xác cao hơn GraphRAG do nó không bị giới hạn bởi cấu trúc của đồ thị.
 - GraphRAG có độ tin cậy cao hơn do nó không bịa thêm thông tin ngoài tài liệu nạp vào.
 - GraphRAG có khả năng trả lời các câu hỏi phức tạp (multi-hop) tốt hơn Flat RAG.
 - Flat RAG có chi phí thấp hơn GraphRAG do nó không cần phải gọi LLM để trích xuất thông tin.
 - GraphRAG có thể dễ dàng mở rộng để xử lý các loại quan hệ mới.

### Phân tích lỗi Ảo giác (Failure Modes Analysis)
Một ví dụ điển hình về ưu điểm của GraphRAG:
- **Câu hỏi**: "Who is the CEO of the company that Alphabet acquired in 2014?"
- **Flat RAG (Lỗi Hallucination)**: Trả lời "Demis Hassabis" (Dựa trên kiến thức ngoài, tài liệu không có thông tin này).
- **GraphRAG (Grounded)**: Trả lời "I don't know" vì đồ thị không có quan hệ CEO.
- **Kết luận**: GraphRAG giúp kiểm soát dữ liệu chặt chẽ hơn, tránh việc AI tự bịa thêm thông tin ngoài tài liệu nạp vào.

## 4. Phân tích Chi phí (Cost Analysis)
Dựa trên quá trình xây dựng và vận hành hệ thống:

- **Token Usage**:
    - **GraphRAG**: Tốn nhiều token hơn (~2.3 lần) do phải gửi danh sách các bộ ba (triplets) lấy từ đồ thị vào Prompt. Tuy nhiên, dữ liệu này có tính cấu trúc cao.
    - **Flat RAG**: Tiết kiệm token hơn vì chỉ lấy các đoạn văn bản thô (chunks).
- **Thời gian (Time)**:
    - **Xây dựng đồ thị (Indexing)**: Tốn thời gian nhất vì phải gọi LLM trích xuất từng thực thể.
    - **Truy vấn (Inference)**: GraphRAG chậm hơn do có thêm bước trung gian (Keyword Extraction & Cypher Query).
- **Tổng kết**: GraphRAG có chi phí vận hành cao hơn nhưng mang lại độ tin cậy (Faithfulness) và khả năng xử lý câu hỏi phức tạp (Multi-hop) tốt hơn so với RAG truyền thống.
