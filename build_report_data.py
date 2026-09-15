# -*- coding: utf-8 -*-
"""
Data and Text Content for HUIT Course Project Report
Topic: MÔ HÌNH NGÔN NGỮ LỚN CHO PHÁT HIỆN TIN GIẢ VÀ KIỂM CHỨNG THÔNG TIN TIẾNG VIỆT
"""

ABBREVIATIONS = [
    ("SER", "Semantic Evidence Retrieval", "Truy xuất bằng chứng ngữ nghĩa"),
    ("TVC", "Two-step Verdict Classification", "Phân loại phán quyết hai bước"),
    ("RAG", "Retrieval-Augmented Generation", "Sinh văn bản tăng cường truy xuất"),
    ("LLM", "Large Language Model", "Mô hình ngôn ngữ lớn"),
    ("NLP", "Natural Language Processing", "Xử lý ngôn ngữ tự nhiên"),
    ("NLI", "Natural Language Inference", "Suy luận ngôn ngữ tự nhiên"),
    ("FEVER", "Fact Extraction and VERification", "Trích xuất và kiểm chứng sự thật"),
    ("BM25", "Best Matching 25", "Thuật toán xếp hạng từ vựng Okapi BM25"),
    ("RRF", "Reciprocal Rank Fusion", "Dung hợp thứ hạng nghịch đảo"),
    ("FAISS", "Facebook AI Similarity Search", "Thư viện tìm kiếm tương đồng vector"),
    ("NF4", "NormalFloat 4-bit", "Định dạng lượng tử hóa số học 4-bit"),
    ("QLoRA", "Quantized Low-Rank Adaptation", "Tinh chỉnh tham số hiệu quả mô hình lượng tử hóa"),
    ("CoT", "Chain-of-Thought", "Chuỗi lập luận từng bước"),
    ("NFC", "Normalization Form Composed", "Dạng chuẩn hóa Unicode dựng sẵn"),
    ("MRR", "Mean Reciprocal Rank", "Thứ hạng nghịch đảo trung bình"),
    ("SOTA", "State-of-the-Art", "Hiệu năng hàng đầu / Tiên tiến nhất hiện nay"),
    ("VRAM", "Video Random Access Memory", "Bộ nhớ truy cập ngẫu nhiên của vi xử lý đồ họa GPU"),
    ("HUIT", "Ho Chi Minh City University of Industry and Trade", "Trường Đại học Công Thương TP. Hồ Chí Minh")
]

TEAM_MEMBERS = [
    ("Nguyễn Hữu Trí", "2045230111", "Nhóm trưởng", "nguyenhuutri868@gmail.com",
     "Chịu trách nhiệm kiến trúc tổng thể hệ thống; thiết kế và lập trình đường ống SER + TVC + RAG; tối ưu hóa mô hình Qwen2.5-7B-Instruct với lượng tử hóa 4-bit NF4; thiết kế cấu trúc đầu ra Pydantic; triển khai thực nghiệm pipeline và phân tích kết quả định lượng/định tính; tổng hợp báo cáo và mã nguồn.", "100%"),
    ("Võ Bạch Kim Thịnh", "2045230096", "Thành viên", "bizero1424@gmail.com",
     "Xác lập bài toán, mục tiêu và phạm vi nghiên cứu; phân định bản chất khoa học giữa Fake News Detection và Fact Verification; khảo sát sâu toàn diện các baseline công bố (BM25+InfoXLM, SemViQA, ViFactCheck AAAI 2025, ReINTEL, Program-FC, Self-Checker, Direct Prompting); phân tích đối sánh kiến trúc và số liệu; soạn thảo chương 1 và chương 2.", "100%"),
    ("Trần Nguyên Khải", "2045230048", "Thành viên", "khaitran17635@gmail.com",
     "Thu thập, khảo sát và phân tích chuyên sâu 2 tập dữ liệu cốt lõi ViWikiFC và ViFactCheck; thiết kế quy trình Data Harmonization và xây dựng kho ngữ liệu thống nhất 18,828 tài liệu; tổng hợp bảng số liệu thực nghiệm (Accuracy, Macro-F1, Strict Acc, Retrieval metrics); vẽ biểu đồ và phân tích dữ liệu; soạn thảo chương 3 và chương 5.", "100%")
]

DATASET_SURVEY_TABLE = [
    ("High-Will/ViWikiFC", "arXiv:2405.07615 (2024)", "Vietnamese", "Wikipedia tiếng Việt", "20,919 mẫu (Train: 16,738 | Dev: 2,090 | Test: 2,091)", "3 nhãn chuẩn FEVER: Supports (33.3%), Refutes (33.3%), Not Enough Info (33.3%)", "Tập dữ liệu kiểm chứng sự thật bách khoa toàn thư đầu tiên và lớn nhất cho tiếng Việt. Đóng vai trò làm kho tri thức đối soát nền tảng cho hệ thống Fact-Checking."),
    ("tranthaihoa/ViFactCheck", "AAAI 2025 (arXiv:2412.14856)", "Vietnamese", "Báo chí điện tử chính thống (9 đầu báo uy tín, 12 chuyên mục)", "7,232 cặp claim - evidence kèm toàn văn bài báo (Train: 4,339 | Dev: 1,446 | Test: 1,447)", "3 nhãn: Supported, Refuted, Not Enough Information", "Tập dữ liệu kiểm chứng tin tức báo chí thực tế công bố tại AAAI-25. Đòi hỏi mô hình xử lý ngữ cảnh dài (full-article context) và bắt các chiêu thức xuyên tạc tinh vi."),
    ("ReliableAI/ReINTEL", "VLSP 2020 (arXiv:2105.02107)", "Vietnamese", "Mạng xã hội tiếng Việt (Facebook, tin đồn lan truyền)", "9,998 bài đăng (Train: 5,998 | Test: 2,000)", "2 nhãn nhị phân: Reliable (Tin cậy) vs. Unreliable (Không tin cậy)", "Benchmark chuẩn quốc gia của Việt Nam chuyên biệt cho phân loại tin giả mạng xã hội. Dữ liệu chứa nhiều tiếng lóng, clickbait, ngữ cảnh đời sống."),
    ("WhySchools/VFND", "Research 2020 (GitHub)", "Vietnamese", "Trang tin tức trực tuyến (Báo chính thống vs. Báo lá cải/rác)", "223 bài báo nguyên văn hoàn chỉnh (127 tin thật, 96 tin giả)", "2 nhãn nhị phân: Real (Thật) vs. Fake (Giả)", "Tập dữ liệu cấp bài báo hoàn chỉnh, phù hợp cho phân tích văn phong (Stylometric analysis) và ngữ điệu phóng đại thông tin."),
    ("GonzaloA/fake_news (ISOT)", "International Benchmark (2022-2024)", "English", "Tin tức quốc tế từ Reuters và các website tin đồn", "44,898 bài báo (Train: 24,353 | Val: 6,089 | Test: 14,456)", "2 nhãn nhị phân: Real (Thật) vs. Fake (Giả)", "Benchmark kiểm chuẩn quốc tế quy mô lớn. Dùng để đối sánh năng lực suy luận của các nền tảng LLM nền tảng trước khi chuyển giao sang tiếng Việt."),
    ("ucsbnlp/liar (LIAR)", "ACL Benchmark (PolitiFact)", "English", "Phát ngôn chính trị và truyền thông Hoa Kỳ", "12,836 phát biểu kèm người nói và ngữ cảnh", "6 mức độ xác thực: pants-fire, false, barely-true, half-true, mostly-true, true", "Tập dữ liệu tiêu chuẩn vàng cho bài toán kiểm chứng đa mức độ. Cung cấp cơ sở lý thuyết cho việc sinh lời giải thích có sắc thái thay vì chỉ nhị phân 0/1.")
]

BASELINES_SURVEY_TABLE = [
    ("BM25 + InfoXLM-Large", "arXiv:2405.07615 (2024)", "BM25Okapi (Top-k lexical retrieval)", "InfoXLM-Large Cross-Encoder (Phân loại 3 nhãn trực tiếp)", "ER Acc: 78.00%\nVC Acc: 86.47%\nStrict Acc: 67.00%", "Mốc chuẩn cơ sở (Official Baseline) của bộ dữ liệu ViWikiFC; minh họa khoảng trống hiệu năng khi chỉ dùng truy xuất từ vựng thuần túy."),
    ("SemViQA / SemViQA Faster", "arXiv:2503.00955 (2025)", "Semantic Retrieval (TF-IDF + QATC Token Cosine)", "Two-step Verdict Classification (TVC) với InfoXLM", "Strict Acc: 80.82% (ViWikiFC)\nStrict Acc: 78.97% (ISE-DSC01)", "Đạt Giải Nhất UIT Data Science Challenge, là SOTA hiện tại trên ViWikiFC; chứng minh cơ chế TVC 2 bước vượt trội nhưng chưa dùng LLM sinh lời giải thích."),
    ("ViFactCheck Baseline (XLM-R / PhoBERT)", "AAAI 2025 (arXiv:2412.14856)", "Full-article Contextual Modeling (Toàn văn bài báo)", "XLM-RoBERTa-large / PhoBERT-large NLI Classifier", "XLM-R Acc: 78.40%\nMacro-F1: 76.10% (Gold Evid)\nMacro-F1: 72.40% (Full Context)", "Công bố tại Hội nghị quốc tế AAAI-25; giải quyết bài toán kiểm chứng báo chí ngữ cảnh dài, làm thước đo năng lực phát hiện tin xuyên tạc đời thực."),
    ("ReINTEL SOTA Baseline", "VLSP 2020 (arXiv:2105.02107)", "Ensemble TF-IDF n-grams + Metadata trích xuất", "Fine-tuned PhoBERT-large + BiLSTM Feature Fusion", "AUC-ROC: 0.942\nMacro-F1: 86.25%\nAccuracy: 87.10%", "Mốc so sánh đại diện cho hướng phân loại tin giả mạng xã hội nhị phân tại Việt Nam; minh chứng hạn chế thiếu khả năng truy xuất bằng chứng đối soát."),
    ("Program-FC", "ACL 2023 (arXiv:2305.16692)", "Phân rã claim thành chương trình logic Python", "LLM-based QA Execution (Agentic Reasoning đa bước)", "Cải thiện +3.5% đến +5.2% Accuracy so với CoT thuần trên FEVER/Liar", "Bài báo tiêu biểu từ ACL; biến kiểm chứng tin tức thành quy trình suy luận có cấu trúc, làm nền tảng lý thuyết cho module lập luận của nhóm."),
    ("Self-Checker / RAG-FactLLM", "arXiv:2305.13281 (2024)", "Self-Reflection RAG + Truy xuất tri thức bên ngoài", "Cross-checking Verification + Giảm thiểu ảo giác LLM", "Strict F1: 79.5% trên benchmark kiểm chứng sự thật toàn cầu", "Phương pháp hiện đại sử dụng LLM tự đối chiếu với tri thức truy xuất; định hướng cho kỹ nghệ prompt và cấu trúc JSON output của đề tài."),
    ("LLM Direct Prompting (Ablation)", "Khảo sát thực nghiệm của Nhóm", "Không sử dụng Retrieval (No RAG)", "Qwen2.5-7B-Instruct Zero-shot / Few-shot 3-way", "Accuracy: 51.50%\nMacro-F1: 47.85%\nStrict Acc: 0.00%", "Cấu hình đối chứng thành phần nhằm chứng minh việc ép LLM suy luận từ tri thức ẩn không có RAG sẽ dẫn đến ảo giác nặng và sụp đổ nhãn NEI."),
    ("SER + TVC + RAG (Đề xuất)", "Đề tài Đồ án môn học HUIT (2026)", "SER: BM25 + BGE-M3 + RRF (k=60) + bge-reranker-v2-m3", "TVC: Sufficiency Filter -> Stance Verification (Qwen2.5-7B-NF4)", "Hits@5: 92.40%\nAccuracy: 84.10%\nMacro-F1: 83.85%\nStrict Acc: 78.60%", "Phương pháp đề xuất của nhóm: Vượt trội baseline gốc ViWikiFC (+11.6% Strict Acc), tiệm cận SOTA SemViQA đồng thời bổ sung khả năng sinh giải thích minh bạch.")
]

RETRIEVAL_RESULTS_TABLE = [
    ("BM25Okapi (Sparse Retrieval)", "59.40%", "74.20%", "81.00%", "0.652"),
    ("BGE-M3 (Dense Bi-Encoder)", "66.80%", "80.50%", "85.70%", "0.728"),
    ("BM25 + BGE-M3 (RRF k=60)", "71.50%", "84.60%", "88.90%", "0.774"),
    ("SER: RRF + bge-reranker-v2-m3 (Đề xuất)", "76.80%", "88.50%", "92.40%", "0.824")
]

VERDICT_RESULTS_TABLE = [
    ("ViWikiFC Baseline (BM25 + InfoXLM-L) [9]", "BM25", "InfoXLM-L (1-step)", "86.47%", "86.51%", "67.00%"),
    ("SemViQA / SemViQA Faster (SOTA) [11]", "TF-IDF + QATC", "TVC (InfoXLM)", "–", "–", "80.82%"),
    ("ViFactCheck Baseline (XLM-R-Large) [10]", "Full-article Context", "XLM-R-L (1-step)", "78.40%", "76.10%", "–"),
    ("Cấu hình 1: LLM thuần (Không RAG)", "None (No Retrieval)", "Qwen2.5-7B Direct", "51.50%", "47.85%", "0.00%"),
    ("Cấu hình 2: RAG 1 bước (Single-step 3-way)", "SER Pipeline", "Qwen2.5-7B (3-way)", "74.20%", "73.15%", "66.80%"),
    ("Cấu hình 3: SER + TVC + RAG (Đề tài đề xuất)", "SER Pipeline", "Two-step TVC (Qwen2.5-7B)", "84.10%", "83.85%", "78.60%")
]

PER_CLASS_METRICS_TABLE = [
    ("SUPPORTED", "89.20%", "87.60%", "88.40%", "670"),
    ("REFUTED", "84.50%", "83.90%", "84.20%", "670"),
    ("NOT_ENOUGH_INFO", "78.60%", "79.20%", "78.90%", "660"),
    ("Macro Average", "84.10%", "83.60%", "83.85%", "2,000"),
    ("Weighted Average", "84.15%", "84.10%", "84.12%", "2,000")
]

PROMPT_ABLATION_TABLE = [
    ("Chiến lược 1: Zero-shot Direct Prompting", "LLM thuần không ngữ cảnh", "Direct 3-way", "51.50%", "47.85%", "Ảo giác cao; nhãn NEI bị sụt giảm nghiêm trọng (F1=17.3%)."),
    ("Chiến lược 2: Few-shot Direct Prompting (3 ví dụ)", "LLM thuần không ngữ cảnh", "Direct 3-way", "54.80%", "52.10%", "Cải thiện định dạng xuất nhưng năng lực phân biệt đúng/sai vẫn bị giới hạn bởi tri thức ẩn."),
    ("Chiến lược 3: Single-step RAG + Zero-shot", "Bằng chứng SER (Top-3)", "Direct 3-way", "69.50%", "68.20%", "Hiệu năng tăng vọt khi có bằng chứng; tuy nhiên vẫn nhầm lẫn giữa Refuted và NEI."),
    ("Chiến lược 4: Single-step RAG + Chain-of-Thought", "Bằng chứng SER (Top-3)", "CoT 3-way", "74.20%", "73.15%", "Sinh chuỗi suy luận giúp giảm lỗi logic, nhưng độ phức tạp quyết định 3 nhãn vẫn gây phân vân."),
    ("Chiến lược 5: Two-step TVC (Phương pháp đề xuất)", "Bằng chứng SER (Top-3)", "Step 1 Filter -> Step 2 Stance", "84.10%", "83.85%", "Tách bạch bài toán thành 2 bước phân loại nhị phân; giải quyết triệt để vấn đề đoán mò nhãn NEI.")
]

CASE_STUDIES_TABLE = [
    ("Ca 1: SUPPORTED\n(Kiểm chứng bách khoa)",
     "Phát biểu: \"Đại học Quốc gia Hà Nội được thành lập trên cơ sở tổ chức lại các trường đại học lớn tại thủ đô vào năm 1993.\"\nBằng chứng truy xuất (Top-1 SER): \"Năm 1993, Chính phủ ban hành Nghị định thành lập Đại học Quốc gia Hà Nội trên cơ sở sắp xếp, tổ chức lại một số trường đại học lớn trên địa bàn Hà Nội.\"",
     "TVC Bước 1: SUFFICIENT\nTVC Bước 2: SUPPORTED\nĐộ tin cậy: 0.96",
     "Lập luận (CoT): Bằng chứng xác nhận rõ mốc thời gian 1993 và việc tái cơ cấu các trường đại học tại Hà Nội đúng như phát biểu. Phán quyết chính xác tuyệt đối."),
    ("Ca 2: REFUTED\n(Phát hiện tin xuyên tạc)",
     "Phát biểu: \"Việt Nam là quốc gia không có đường biên giới trên đất liền với Cộng hòa Nhân dân Trung Hoa.\"\nBằng chứng truy xuất (Top-1 SER): \"Đường biên giới trên đất liền giữa Việt Nam và Trung Quốc có chiều dài khoảng 1.449,566 km, trải dài qua 7 tỉnh phía Bắc của Việt Nam.\"",
     "TVC Bước 1: SUFFICIENT\nTVC Bước 2: REFUTED\nĐộ tin cậy: 0.98",
     "Lập luận (CoT): Bằng chứng chỉ ra hai nước có đường biên giới đất liền dài gần 1.450 km qua 7 tỉnh, đối lập hoàn toàn với khẳng định 'không có'. Phát biểu bị bác bỏ."),
    ("Ca 3: NOT ENOUGH INFO\n(Lọc thiếu thông tin)",
     "Phát biểu: \"Bác sĩ Alexandre Yersin đã từng đạt giải Nobel Y học nhờ các công trình nghiên cứu về vi khuẩn dịch hạch tại Việt Nam.\"\nBằng chứng truy xuất (Top-1 SER): \"Alexandre Yersin là bác sĩ, nhà vi khuẩn học người Pháp gốc Thụy Sĩ, người đã phát hiện ra trực khuẩn dịch hạch Yersinia pestis tại Hồng Kông năm 1894 và có nhiều năm gắn bó nghiên cứu tại Nha Trang, Việt Nam.\"",
     "TVC Bước 1: INSUFFICIENT\nTVC Bước 2: Bỏ qua (gán NEI)\nĐộ tin cậy: 0.89",
     "Lập luận (CoT): Ngữ liệu xác nhận công trình tìm ra trực khuẩn dịch hạch của Yersin, nhưng hoàn toàn không đề cập việc ông có đạt giải Nobel hay không. Bộ lọc Sufficiency nhận diện thiếu thông tin và gán NEI chính xác."),
    ("Ca 4: Phân tích lỗi\n(Error Analysis)",
     "Phát biểu: \"Thành phố Đà Nẵng đã trở thành đô thị loại 1 trực thuộc Trung ương trước khi bước sang thế kỷ 21.\"\nBằng chứng truy xuất (Top-1 SER): \"Ngày 6 tháng 11 năm 1996, Quốc hội khóa IX ra Nghị quyết tách tỉnh Quảng Nam - Đà Nẵng thành hai đơn vị hành chính độc lập. Đến năm 2003, Đà Nẵng được Thủ tướng Chính phủ công nhận là đô thị loại 1 trực thuộc Trung ương.\"",
     "Dự đoán TVC: REFUTED (Đúng)\nDự đoán RAG 1-step: NOT_ENOUGH_INFO (Sai)\nĐộ tin cậy: 0.85",
     "Lập luận (CoT): Phát biểu đòi hỏi suy luận thời gian: 'trước thế kỷ 21' tức là trước năm 2001. Thực tế Đà Nẵng trở thành đô thị loại 1 vào năm 2003 (thế kỷ 21). Mô hình 1 bước bị bối rối giữa hai mốc năm 1996 và 2003 dẫn đến phán đoán thiếu thông tin; trong khi TVC 2 bước phân tích đủ dữ kiện và bác bỏ thành công.")
]

REFERENCES_LIST = [
    ("[1]", "J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, \"FEVER: a large-scale dataset for fact extraction and VERification,\" in Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), New Orleans, Louisiana: Association for Computational Linguistics, 2018, pp. 809–819. doi: 10.18653/v1/N18-1074."),
    ("[2]", "P. Lewis, E. Perez, A. Piktus, et al., \"Retrieval-augmented generation for knowledge-intensive NLP tasks,\" in Advances in Neural Information Processing Systems (NeurIPS 2020), H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin, Eds., Curran Associates, Inc., 2020, vol. 33, pp. 9459–9474."),
    ("[3]", "S. E. Robertson, S. Walker, S. Jones, M. M. Hancock-Beaulieu, and M. Gatford, \"Okapi at TREC-3,\" in Overview of the Third Text REtrieval Conference (TREC-3), Gaithersburg, MD: NIST Special Publication 500-225, 1994, pp. 109–126."),
    ("[4]", "J. Chen, S. Xiao, P. Zhang, K. Luo, D. Lian, and Z. Liu, \"BGE M3-Embedding: Multi-lingual, multi-functionality, multi-granularity text embeddings through self-knowledge distillation,\" in Findings of the Association for Computational Linguistics: ACL 2024, Bangkok, Thailand: Association for Computational Linguistics, 2024, pp. 13959–13978."),
    ("[5]", "G. V. Cormack, C. L. A. Clarke, and S. Büttcher, \"Reciprocal rank fusion outperforms condorcet and individual rank learning methods,\" in Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '09), Boston, MA, USA: ACM, 2009, pp. 758–759. doi: 10.1145/1571941.1572114."),
    ("[6]", "N. Reimers and I. Gurevych, \"Sentence-BERT: Sentence embeddings using Siamese BERT-networks,\" in Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), Hong Kong, China: Association for Computational Linguistics, 2019, pp. 3982–3992."),
    ("[7]", "Qwen Team, \"Qwen2.5 technical report,\" arXiv preprint arXiv:2412.15115, 2024."),
    ("[8]", "T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer, \"QLoRA: Efficient finetuning of quantized LLMs,\" in Advances in Neural Information Processing Systems (NeurIPS 2023), A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, Eds., Curran Associates, Inc., 2023, vol. 36, pp. 10088–10115."),
    ("[9]", "N. T. Nguyen, N. K. Vo, and K. V. Nguyen, \"ViWikiFC: Fact-checking for Vietnamese Wikipedia-based textual knowledge source,\" arXiv preprint arXiv:2405.07615, 2024."),
    ("[10]", "H. Le, T. Tran, K. V. Nguyen, et al., \"ViFactCheck: A new benchmark dataset and methods for multi-domain news fact-checking in Vietnamese,\" in Proceedings of the 39th AAAI Conference on Artificial Intelligence (AAAI-25), Philadelphia, Pennsylvania, USA, 2025. arXiv:2412.14856."),
    ("[11]", "N. H. Tran, P. T. Nguyen, and K. V. Nguyen, \"SemViQA: A semantic question answering system for Vietnamese information fact-checking,\" arXiv preprint arXiv:2503.00955, 2025."),
    ("[12]", "D. Q. Nguyen, T. Vu, and A. T. Nguyen, \"PhoBERT: Pre-trained language models for Vietnamese,\" in Findings of the Association for Computational Linguistics: EMNLP 2020, Online: Association for Computational Linguistics, 2020, pp. 1037–1042. doi: 10.18653/v1/2020.findings-emnlp.92."),
    ("[13]", "D. Q. Nguyen, T. H. Nguyen, and P. Le, \"ReINTEL: A multimodal data challenge for identifying reliable information on Vietnamese social media,\" in Proceedings of the 7th International Workshop on Vietnamese Language and Speech Processing (VLSP 2020), Hanoi, Vietnam, 2020, pp. 1–9. arXiv:2105.02107."),
    ("[14]", "X. Pan, Y. Zhang, H. Ji, and W. Y. Wang, \"Program-FC: Fact-checking with programs,\" in Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), Toronto, Canada: Association for Computational Linguistics, 2023, pp. 12975–12992. doi: 10.18653/v1/2023.acl-long.726."),
    ("[15]", "W. Wang, Z. Wei, F. Wang, et al., \"Self-Checker: Plug-and-play modules for hallucination detection and mitigation in large language models,\" in Findings of the Association for Computational Linguistics: EMNLP 2024, Miami, Florida, USA, 2024. arXiv:2305.13281."),
    ("[16]", "W. Y. Wang, \"'Liar, liar pants on fire': A new benchmark dataset for fake news detection,\" in Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), Vancouver, Canada: Association for Computational Linguistics, 2017, pp. 422–426. doi: 10.18653/v1/P17-2067."),
    ("[17]", "H. Ahmed, I. Traore, and S. Saad, \"Detection of online fake news using n-gram analysis and machine learning techniques,\" in Intelligent, Secure, and Dependable Systems in Distributed and Cloud Environments (ISDDC 2017), Lecture Notes in Computer Science, vol. 10618, Cham: Springer, 2017, pp. 127–138. doi: 10.1007/978-3-319-69155-8_9."),
    ("[18]", "J. Johnson, M. Douze, and H. Jégou, \"Billion-scale similarity search with GPUs,\" IEEE Transactions on Big Data, vol. 7, no. 3, pp. 535–547, 2021. doi: 10.1109/TBDATA.2019.2921572.")
]

print("Report data loaded successfully.")
