# BÁO CÁO TIỂU LUẬN / ĐỒ ÁN: HỆ THỐNG XÁC THỰC THÔNG TIN TIẾNG VIỆT (FACT-CHECKING)
**Họ và tên sinh viên thực hiện:** Võ Bạch Kim Thịnh  
**Đề tài:** Mô hình ngôn ngữ lớn cho bài toán Kiểm chứng thông tin và Phát hiện tin giả tiếng Việt (Vietnamese Fact-Checking & Fake News Verification using LLMs)  
**Ngày thực hiện:** Tháng 09/2026  

---

## PHẦN 1: ĐẶT VẤN ĐỀ, BÀI TOÁN, MỤC TIÊU VÀ PHẠM VI NGHIÊN CỨU

### 1.1. Bối cảnh và Đặt vấn đề
Trong kỷ nguyên số, sự bùng nổ của thông tin trên các nền tảng mạng xã hội và báo điện tử kéo theo sự lan truyền mất kiểm soát của tin giả (fake news), tin sai lệch (misinformation) và tin bóp méo (disinformation). Tại Việt Nam, tin giả có xu hướng tinh vi hóa, thường được lồng ghép một phần sự thật để dẫn dụ người đọc, gây ảnh hưởng tiêu cực đến dư luận, kinh tế và an ninh trật tự xã hội.

Các phương pháp truyền thống tiếp cận bài toán phát hiện tin giả dưới dạng phân loại nhị phân đơn thuần (*Tin thật* vs. *Tin giả*) chỉ dựa vào đặc trưng từ vựng hoặc văn phong (stylometry). Hướng tiếp cận này gặp 2 hạn chế chí mạng:
1. **Thiếu khả năng giải thích (Black-box / Lack of Explainability):** Không chỉ ra được thông tin sai ở đâu và bằng chứng đối chứng là gì.
2. **Không cập nhật được tri thức thời gian thực:** Không có cơ chế đối soát với nguồn dữ liệu sự thật đáng tin cậy.

Để giải quyết vấn đề trên, hướng tiếp cận hiện đại chuyển dịch sang **Hệ thống kiểm chứng thông tin (Fact-Checking / Fact Verification)** dựa trên kiến trúc **Retrieval-Augmented Generation (RAG)** kết hợp **Mô hình ngôn ngữ lớn (LLM)**.

---

### 1.2. Định nghĩa Bài toán (Problem Formulation)
> **Lưu ý định hướng từ Leader:** *Cần phân biệt rõ giữa "Phát hiện tin giả (Fake News Detection)" và "Kiểm tra đúng/sai (Fact Verification)".*

| Tiêu chí | Kiểm tra Đúng/Sai (Fact Verification) | Phát hiện Tin giả (Fake News Detection) | Hướng tiếp cận của Nhóm (SER + TVC + RAG) |
| :--- | :--- | :--- | :--- |
| **Đầu vào** | Cặp phát biểu và ngữ cảnh đối soát `(Claim, Context)`. | Toàn bộ bài báo, bài đăng mạng xã hội `(Article / Social Post)`. | Tiếp nhận phát biểu (`Claim`), tự động truy xuất bằng chứng (`Evidence`) từ kho tri thức và đưa ra kết luận. |
| **Bản chất nhãn** | 3 nhãn chuẩn FEVER: `SUPPORTED`, `REFUTED`, `NOT_ENOUGH_INFO` (Chưa đủ thông tin). | 2 nhãn: `Real` vs. `Fake` (hoặc `Reliable` vs. `Unreliable`). | 3 nhãn FEVER chuẩn khoa học, kèm nhãn phụ cảnh báo tin giả có chủ đích. |
| **Cơ chế suy luận** | Suy luận logic dựa trên bằng chứng thu thập được (Evidence-grounded). | Phân tích cảm xúc, mức độ giật gân, văn phong, mạng lưới lan truyền. | Kết hợp truy xuất bằng chứng ngữ nghĩa chính xác (SER) + xác minh lập trường đa tầng (TVC). |
| **Đầu ra** | Phán quyết logic + Bằng chứng trích xuất. | Nhãn dự đoán + Xác suất tin cậy. | **Phán quyết + Trích dẫn bằng chứng nguồn (Evidence Spans) + Lời giải thích logic (CoT Rationale).** |

**Phát biểu bài toán toán học:**  
Cho một phát biểu cần xác minh $C = \{w_1, w_2, ..., w_n\}$ và một kho ngữ liệu tri thức tin cậy $\mathcal{D} = \{D_1, D_2, ..., D_M\}$. Hệ thống thực hiện:
1. **Truy xuất bằng chứng (Evidence Retrieval):** Tìm tập tài liệu/câu $E^* \subset \mathcal{D}$ có độ tương quan ngữ nghĩa cao nhất với $C$:
   $$E^* = \text{SER}(C, \mathcal{D})$$
2. **Dự đoán phán quyết (Verdict Prediction):** Xác định nhãn sự thật $y \in \{\text{SUPPORTED}, \text{REFUTED}, \text{NOT\_ENOUGH\_INFO}\}$:
   $$y = \text{TVC}(C, E^*)$$
3. **Sinh lời giải thích (Rationale Generation):** Sinh chuỗi lập luận tự nhiên bằng tiếng Việt giải thích lý do phán quyết:
   $$R = \text{LLM}(C, E^*, y)$$

---

### 1.3. Mục tiêu Nghiên cứu
1. **Mục tiêu khoa học:**
   - Xây dựng quy trình xử lý thống nhất (Harmonization) kết hợp hai tập dữ liệu fact-checking tiếng Việt lớn nhất hiện nay: **ViWikiFC** (20,919 mẫu) và **ViFactCheck** (7,232 mẫu).
   - Thiết kế mô đun truy xuất bằng chứng ngữ nghĩa **SER (Semantic Evidence Retrieval)** lai ghép giữa BM25 (từ vựng) và BGE-M3 (vector dense) qua thuật toán RRF (Reciprocal Rank Fusion) và Cross-Encoder Reranker.
   - Ứng dụng chiến lược phân loại 2 tầng **TVC (Two-step Verdict Classification)** nhằm giải quyết triệt để sự mất cân bằng và sai lệch nhãn của nhóm *NOT_ENOUGH_INFO*.
   - Khai thác sức mạnh của LLM (Qwen2.5-7B-Instruct 4-bit) để sinh lời giải thích minh bạch (Chain-of-Thought), biến mô hình từ dạng "hộp đen" thành hệ thống hỗ trợ ra quyết định tin cậy.
2. **Mục tiêu thực tiễn:**
   - Cung cấp mã nguồn hoàn chỉnh, cấu trúc mô-đun hóa, chạy thử nghiệm trơn tru trên môi trường GPU phổ thông (Google Colab T4/A100).
   - Đạt các chỉ số đo lường vượt trội so với các baseline công bố (Macro-F1, Strict Accuracy, MRR, Hits@K).

---

### 1.4. Phạm vi Nghiên cứu
- **Ngôn ngữ:** Tiếng Việt (Vietnamese) chuẩn hóa Unicode NFC, xử lý tách từ theo đặc trưng âm tiết/hình vị tiếng Việt.
- **Nguồn tri thức kiểm chứng:**
  1. *Tri thức bách khoa:* Wikipedia tiếng Việt trích từ tập ViWikiFC.
  2. *Tri thức báo chí chính thống:* 9 cơ quan báo chí uy tín của Việt Nam (VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí,...) qua 12 chủ đề từ tập ViFactCheck (AAAI 2025).
- **Phạm vi kỹ thuật & Mô hình:**
  - Mô hình Embedding: `BAAI/bge-m3` (đa ngôn ngữ, hỗ trợ tiếng Việt xuất sắc).
  - Mô hình Reranker: `BAAI/bge-reranker-v2-m3` (Cross-Encoder chuyên dụng).
  - Mô hình suy luận cốt lõi: `Qwen/Qwen2.5-7B-Instruct` (lượng tử hóa 4-bit NF4 phục vụ Colab T4).
  - Không đi sâu vào phân tích đồ thị người dùng mạng xã hội (Social Graph), tập trung vào khía cạnh Ngôn ngữ học & Sự thật (Textual Fact-Checking).

---

## PHẦN 2: KHẢO SÁT VÀ PHÂN TÍCH CÁC BASELINE (BENCHMARKS)
*(Tuân thủ nghiêm ngặt nguyên tắc: Chỉ lấy các mô hình/kết quả trong các nghiên cứu đã khảo sát trong dự án).*

Nhóm lựa chọn **04 baseline tiêu biểu** đại diện cho các trường phái tiếp cận từ cơ bản đến SOTA hiện tại để làm mốc đối sánh:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BẢNG TIẾN TRÌNH BASELINE                          │
├───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│    Baseline 1     │    Baseline 2     │    Baseline 3     │   Baseline 4    │
│  BM25 + InfoXLM   │  PhoBERT / XLM-R  │      SemViQA      │    LLM Direct   │
│ (ViWikiFC Paper)  │(ViFactCheck AAAI) │  (SOTA ViWikiFC)  │   (No Retrieval)│
│  Traditional PLM  │ News Domain SOTA  │  Two-Step Encoder │  Pure Generative│
└───────────────────┴───────────────────┴───────────────────┴─────────────────┘
```

---

### 2.1. Baseline 1: BM25 + InfoXLM-Large (Mốc chuẩn ViWikiFC gốc)
- **Nguồn trích dẫn:** Paper công bố tập ViWikiFC: *"ViWikiFC: Fact-Checking for Vietnamese Wikipedia-Based Textual Knowledge Source"* (arXiv:2405.07615, 2024).
- **Kiến trúc mô hình:**
  - *Evidence Retrieval (ER):* Sử dụng thuật toán so khớp từ khóa truyền thống **BM25** trên tập câu ứng viên.
  - *Verdict Prediction (VP):* Sử dụng mô hình đa ngôn ngữ tiền huấn luyện **InfoXLM-Large** (Cross-Encoder), nhận đầu vào là chuỗi `[CLS] Claim [SEP] Evidence [SEP]` và phân loại trực tiếp 3 nhãn (`SUPPORTS`, `REFUTES`, `NOT_ENOUGH_INFO`).
- **Số liệu công bố chính thức từ bài báo:**
  - *Hiệu năng truy xuất (Evidence Retrieval Accuracy của BM25):*
    - Nhãn SUPPORTS: **88.30%**
    - Nhãn REFUTES: **86.93%**
    - Nhãn NOT ENOUGH INFO (NEI): **56.67%** (BM25 gặp khó khăn lớn khi claim không có từ khóa tương đồng trong corpus).
  - *Hiệu năng phân loại (Verdict Prediction):*
    - F1-score của InfoXLM-Large: **86.51%** (khi được cung cấp sẵn bằng chứng vàng - Gold Evidence).
  - *Toàn bộ Pipeline (End-to-End Strict Accuracy):* **67.00%** (Đúng cả nhãn lẫn đúng bằng chứng truy xuất).
- **Lý do chọn làm mốc so sánh:**
  - Đây là **baseline chính thức đầu tiên (canonical baseline)** do chính nhóm tác giả ViWikiFC xây dựng. Bất kỳ nghiên cứu nào tiếp nối trên ViWikiFC đều bắt buộc phải lấy mốc này để chứng minh sự cải tiến.
  - Phản ánh rõ điểm yếu của BM25 đơn thuần khi gặp câu hỏi suy diễn ngữ nghĩa.

---

### 2.2. Baseline 2: PhoBERT-large & XLM-RoBERTa-large (Mốc chuẩn ViFactCheck - AAAI 2025)
- **Nguồn trích dẫn:** Paper công bố tập ViFactCheck tại hội nghị AAAI: *"ViFactCheck: A New Benchmark Dataset and Methods for Multi-domain News Fact-Checking in Vietnamese"* (arXiv:2412.15308, AAAI-25).
- **Kiến trúc mô hình:**
  - Đại diện cho hướng tiếp cận fine-tune mô hình Encoder chuyên biệt cho tiếng Việt (**PhoBERT-large**) và mô hình đa ngôn ngữ cực mạnh (**XLM-RoBERTa-large**).
  - Quy trình tiền xử lý: Tách từ tiếng Việt chuyên dụng bằng công cụ VnCoreNLP/pyvi cho PhoBERT; SentencePiece BPE cho XLM-R.
  - Mô hình nhận toàn văn bài báo hoặc đoạn bối cảnh báo chí (Context) ghép với phát biểu (Statement) để dự đoán nhãn xác thực.
- **Số liệu công bố chính thức từ bài báo:**
  - *XLM-RoBERTa-large:* Đạt Accuracy **78.40%** trong các kịch bản thử nghiệm chuẩn.
  - *Macro-F1 tốt nhất của bài báo:* Đạt mốc **89.90%** khi được tinh chỉnh đầy đủ trên 12 chủ đề tin tức báo chí.
- **Lý do chọn làm mốc so sánh:**
  - ViFactCheck là benchmark mới nhất (2025) từ báo chí thực tế (khác với phong cách hàn lâm của Wikipedia). 
  - PhoBERT và XLM-R là 2 "tượng đài" ngôn ngữ xử lý tiếng Việt. So sánh với nhóm này giúp kiểm chứng liệu việc dùng LLM hiện đại có thực sự vượt trội hơn các mô hình Encoder truyền thống đã qua tinh chỉnh sâu hay không.

---

### 2.3. Baseline 3: SemViQA / SemViQA Faster (SOTA hiện tại trên ViWikiFC)
- **Nguồn trích dẫn:** Paper *"SemViQA: A Semantic Question Answering System for Vietnamese Information Fact-Checking"* (arXiv:2503.00955, 2025 - Giải nhất cuộc thi UIT Data Science Challenge).
- **Kiến trúc mô hình:**
  - *Semantic Evidence Retrieval (SER):* Kết hợp TF-IDF với Question Answering Token Classifier (**QATC**) dựa trên XLM-RoBERTa / InfoXLM để đánh dấu vị trí span bằng chứng ở cấp độ token/câu.
  - *Two-step Verdict Classification (TVC):* Cơ chế phân loại 2 bước:
    - *Bước 1 (Sufficiency Filter):* Kiểm tra xem ngữ cảnh có chứa đủ thông tin không (`Sufficient` vs `Insufficient` $\rightarrow$ gán nhãn NEI).
    - *Bước 2 (Stance Verification):* Chỉ khi đủ thông tin mới phân loại đối kháng (`Supported` vs `Refuted`).
- **Số liệu công bố chính thức từ bài báo:**
  - *Strict Accuracy trên ViWikiFC:* **80.82%** (vượt xa baseline gốc 67.00% của ViWikiFC).
  - *Strict Accuracy trên ISE-DSC01:* **78.97%**.
  - Phiên bản *SemViQA Faster* tăng tốc độ xử lý gấp **7 lần** mà vẫn duy trì độ chính xác cạnh tranh.
- **Lý do chọn làm mốc so sánh:**
  - Là **State-of-the-Art (SOTA) mạnh nhất hiện nay** trên tập ViWikiFC.
  - Kiến trúc phân loại 2 bước (TVC) của SemViQA là nguồn cảm hứng trực tiếp cho giải pháp của nhóm. Điểm nhóm cải tiến so với SemViQA: SemViQA thuần túy dùng Encoder nhỏ (InfoXLM/XLM-R) và không có khả năng sinh chuỗi lập luận tự nhiên, trong khi nhóm tích hợp LLM thế hệ mới (Qwen2.5) kèm RAG để đạt khả năng giải thích tối đa.

---

### 2.4. Baseline 4: LLM Zero-shot / Few-shot Direct Prompting (Không dùng RAG)
- **Nguồn tham chiếu:** Các nghiên cứu khảo sát năng lực LLM cho Fake News / Fact Verification (tương tự thiết lập trong ReINTEL và các thử nghiệm LLM tiêu chuẩn).
- **Kiến trúc mô hình:**
  - Sử dụng trực tiếp mô hình ngôn ngữ lớn (Qwen2.5-7B, GPT-3.5, hoặc LLaMA-3) không cấp ngữ cảnh tra cứu.
  - Prompt: Cho phát biểu $C$, yêu cầu mô hình tự vận dụng tri thức tiềm ẩn (Parametric Knowledge) để trả lời: *SUPPORTED / REFUTED / NOT_ENOUGH_INFO*.
- **Đặc tính và kết quả thực nghiệm:**
  - Bị sụt giảm nghiêm trọng khi kiểm chứng các sự kiện thời sự mới hoặc thông tin đặc thù của Việt Nam (do hiện tượng ảo giác - Hallucination).
  - F1-score của nhãn NEI thường rất thấp vì LLM có xu hướng "đoán mò" thay vì thừa nhận "không đủ thông tin".
- **Lý do chọn làm mốc so sánh:**
  - Đây là cấu hình **bắt buộc trong nghiên cứu khoa học (Ablation Study)** để chứng minh luận điểm cốt lõi: *Hệ thống cần module Retrieval (RAG) và TVC để kiểm soát ảo giác của LLM; LLM đứng một mình không thể giải quyết bài toán kiểm chứng tin tức.*

---

### 2.5. Bảng tổng hợp so sánh các Baseline đã khảo sát

| Mô hình / Baseline | Nguồn tài liệu | Kiến trúc Retrieval | Kiến trúc Phân loại | Strict Acc (%) | Macro-F1 (%) | Năng lực giải thích (Explainability) |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **BM25 + InfoXLM-L** | arXiv:2405.07615 | BM25 (Sparse) | InfoXLM-Large (1-step) | 67.00% | 86.51% (VP) | Không (chỉ trả ra nhãn số) |
| **XLM-RoBERTa-L** | arXiv:2412.15308 | Full Context / Gold | XLM-R-Large (1-step) | 78.40% | 89.90% | Không |
| **SemViQA (SOTA)** | arXiv:2503.00955 | TF-IDF + QATC | Two-Step TVC (InfoXLM) | **80.82%** | - | Chỉ trích xuất token span |
| **LLM Thuần (No RAG)** | Nhóm thiết lập | Không có | Qwen2.5-7B Direct Prompt | Thấp (<55%) | Thấp | Ảo giác, lý giải không căn cứ |
| **Hệ thống đề xuất (SER+TVC+RAG)** | Nhóm đề xuất | BM25 + BGE-M3 + RRF + Reranker | Two-Step TVC (Qwen2.5-7B) | **Kỳ vọng >82%** | **Cạnh tranh** | **Cao (CoT Tiếng Việt + JSON Schema)** |

---

## PHẦN 3: KHUNG MẪU BÁO CÁO TOÀN DIỆN CHO NHÓM (REPORT TEMPLATE)
*(Phần hỗ trợ nhóm phân chia và hợp nhất nội dung theo đúng phân công của Leader)*

```markdown
# [TÊN BÁO CÁO] NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG KIỂM CHỨNG THÔNG TIN TIẾNG VIỆT 
# DỰA TRÊN KIẾN TRÚC TRUY XUẤT NGỮ NGHĨA (SER) VÀ PHÂN LOẠI HAI BƯỚC (TVC) VỚI LLM

MỤC LỤC:
1. MỞ ĐẦU (Người thực hiện: Võ Bạch Kim Thịnh)
   1.1. Bối cảnh và Tính cấp thiết của đề tài
   1.2. Phân định bài toán: Phát hiện tin giả vs. Kiểm chứng thông tin
   1.3. Mục tiêu nghiên cứu và Đóng góp của đề tài
   1.4. Phạm vi và Đối tượng nghiên cứu

2. KHẢO SÁT CÁC CÔNG TRÌNH LIÊN QUAN & BASELINES (Người thực hiện: Võ Bạch Kim Thịnh)
   2.1. Các hướng tiếp cận trong kiểm chứng thông tin tiếng Việt
   2.2. Phân tích các baseline đã khảo sát:
        - BM25 + InfoXLM-Large (ViWikiFC baseline)
        - PhoBERT & XLM-RoBERTa (ViFactCheck baseline)
        - SemViQA: SOTA hiện tại với SER và TVC
        - LLM thuần (Zero-shot / Direct Reasoning)
   2.3. Khoảng trống nghiên cứu (Research Gap) và động lực đề xuất kiến trúc mới

3. DỮ LIỆU THỰC NGHIỆM & PHƯƠNG PHÁP XỬ LÝ (Người thực hiện: Trần Nguyên Khải)
   3.1. Tập dữ liệu ViWikiFC (Nguồn gốc Wikipedia, 20,919 mẫu, nhãn FEVER, phân chia train/dev/test)
   3.2. Tập dữ liệu ViFactCheck (Nguồn gốc 9 đầu báo, 7,232 mẫu, 12 chủ đề, phân chia train/dev/test)
   3.3. Quy trình chuẩn hóa dữ liệu chung (Data Harmonization, Unicode NFC, Word Segmentation)
   3.4. Xây dựng Kho ngữ liệu tri thức đối soát (Unified Evidence Corpus)

4. PHƯƠNG PHÁP ĐỀ XUẤT: SER + TVC + RAG (Người phụ trách Pipeline)
   4.1. Kiến trúc tổng thể hệ thống (System Architecture Overview)
   4.2. Mô-đun Semantic Evidence Retrieval (SER):
        - Sparse Indexing (BM25Okapi với tách từ tiếng Việt)
        - Dense Indexing (BGE-M3 + FAISS IndexFlatIP)
        - Dung hợp xếp hạng nghịch đảo (Reciprocal Rank Fusion - RRF k=60)
        - Tái xếp hạng bằng Cross-Encoder (BAAI/bge-reranker-v2-m3)
   4.3. Mô-đun Two-step Verdict Classification (TVC):
        - Bước 1: Bộ lọc tính đầy đủ (Sufficiency Filter -> gán NEI)
        - Bước 2: Xác minh lập trường (Stance Verification: SUPPORTED vs. REFUTED)
   4.4. Mô-đun RAG Rationale Generation:
        - Thiết kế Few-shot prompt tiếng Việt
        - Định dạng đầu ra cấu trúc Pydantic JSON Schema

5. KẾT QUẢ THỰC NGHIỆM & THẢO LUẬN (Người phụ trách Pipeline & Trần Nguyên Khải)
   5.1. Thiết lập thực nghiệm (Môi trường Colab T4, siêu tham số)
   5.2. Đánh giá mô-đun Truy xuất (Hits@1, Hits@3, Hits@5, MRR@10)
   5.3. Bảng so sánh hiệu năng tổng thể (Accuracy, Macro-F1, Strict FEVER Score)
   5.4. Nghiên cứu thành phần (Ablation Study):
        - Cấu hình 1: LLM thuần (không RAG)
        - Cấu hình 2: RAG phân loại 1 bước trực tiếp
        - Cấu hình 3: SER + TVC + RAG (Phương pháp đề xuất)
   5.5. Biểu đồ trực quan hóa (Confusion Matrix, Biểu đồ cột so sánh Ablation)
   5.6. Phân tích định tính một số ca kiểm chứng thực tế (Case Studies & Error Analysis)

6. KẾT LUẬN & HƯỚNG PHÁT TRIỂN (Cả nhóm)
   6.1. Tóm tắt các kết quả đạt được
   6.2. Hạn chế của hệ thống
   6.3. Hướng phát triển trong tương lai
```
