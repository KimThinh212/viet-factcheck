# Lược Đồ Dữ Liệu ViWikiFC (Dataset Schema)

## 1. Nguồn Gốc & Trích Dẫn
- **Kho lưu trữ Hugging Face**: [High-Will/ViWikiFC](https://huggingface.co/datasets/High-Will/ViWikiFC)
- **Bài báo gốc**: *ViWikiFC: Fact-Checking for Vietnamese Wikipedia-Based Textual Knowledge Source* ([arXiv:2405.07615](https://arxiv.org/abs/2405.07615))
- **Ngôn ngữ**: Tiếng Việt (`vi`)
- **Miền dữ liệu**: Kiểm chứng thông tin từ bách khoa toàn thư Wikipedia

## 2. Phân Chia Tập Dữ Liệu
| Phân tập | Số lượng mẫu | Supports | Refutes | Not_Enough_Information | Đường dẫn |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | 16,738 | 5,594 | 5,573 | 5,571 | `data/raw/train.csv` |
| **Dev / Val** | 2,090 | 666 | 694 | 730 | `data/raw/dev.csv` |
| **Test** | 2,091 | 708 | 706 | 677 | `data/raw/test.csv` |
| **Tổng cộng** | **20,919** | **6,968** | **6,973** | **6,978** | |

Tỷ lệ nhãn phân bổ đồng đều tuyệt đối (mỗi nhãn chiếm ~33.3%).

## 3. Lược Đồ Các Cột (Columns Schema)

| Tên Cột | Kiểu Dữ Liệu | Ý Nghĩa / Mô Tả | Ví Dụ |
| :--- | :--- | :--- | :--- |
| `pairID` | String | Mã định danh duy nhất của cặp phát biểu - bằng chứng | `uit_424_27_39_3_11` |
| `sentenceID` | String | Mã định danh câu gốc trong ngữ cảnh | `uit_424_27_39_3` |
| `claim` | String | Phát biểu cần kiểm chứng tính đúng/sai | `Chế độ quân chủ chuyên chế của nhà Thanh...` |
| `context` | String | Đoạn văn bản bách khoa trích từ Wikipedia | `Cuối thời nhà Thanh, do sự lạc hậu về...` |
| `evidence` | String | Câu bằng chứng đối soát chính xác | `Chế độ quân chủ chuyên chế đã tỏ ra...` |
| `gold_label` | String | Nhãn kiểm chứng: `Supports`, `Refutes`, `Not_Enough_Information` | `Supports` |
| `annotator_labels`| List / Str | Nhãn do từng chuyên viên gán nhãn đánh giá | `['Support']` |
| `title` | String | Tiêu đề trang bài viết Wikipedia | `Trung Quốc` |
| `link` | String | Liên kết tới bài viết Wikipedia gốc | `https://vi.wikipedia.org/Trung Quốc` |

## 4. Các Nhiệm Vụ Trong Đề Tài

1. **Truy xuất bằng chứng (Evidence Retrieval - ER)**: Từ phát biểu và bài viết Wikipedia, tự động truy xuất câu làm bằng chứng.
2. **Phân loại xác thực (Verdict Classification - VC)**: Từ cặp `(Claim, Evidence)`, phân loại 3 nhãn:
   - `Supports`: Bằng chứng chứng minh phát biểu là Đúng.
   - `Refutes`: Bằng chứng chứng minh phát biểu là Sai.
   - `Not_Enough_Information`: Ngữ cảnh không đủ căn cứ để kết luận.
3. **Pipeline hoàn chỉnh (Full Pipeline)**: Kết hợp cả hai bước ER và VC từ câu phát biểu bất kỳ.