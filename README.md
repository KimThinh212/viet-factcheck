# Viet-Factcheck: Vietnamese Information Fact-Checking System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![HuggingFace Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-High--Will%2FViWikiFC-yellow)](https://huggingface.co/datasets/High-Will/ViWikiFC)
[![Paper](https://img.shields.io/badge/arXiv-2405.07615-b31b1b.svg)](https://arxiv.org/abs/2405.07615)

Dự án **Viet-Factcheck** là hệ thống kiểm chứng tính xác thực của các phát biểu (Fact-Checking / Claim Verification) dựa trên nguồn tri thức bách khoa toàn thư tiếng Việt (Wikipedia). Hệ thống giải quyết bài toán: đối soát một phát biểu (`claim`), truy xuất bằng chứng đối soát (`evidence`) từ văn bản ngữ cảnh (`context`), và phân loại nhãn xác thực (`Supports`, `Refutes`, `Not_Enough_Information`).

---

## 📌 Nguồn Dữ Liệu (Dataset Attribution)

Dữ liệu được sử dụng trong dự án này là bộ dữ liệu gốc **ViWikiFC** (Vietnamese Wikipedia Fact-Checking Dataset):
- **Kho lưu trữ Hugging Face**: [High-Will/ViWikiFC](https://huggingface.co/datasets/High-Will/ViWikiFC)
- **Tác giả & Bài báo gốc**: *ViWikiFC: Fact-Checking for Vietnamese Wikipedia-Based Textual Knowledge Source* ([arXiv:2405.07615](https://arxiv.org/abs/2405.07615)).
- **Dữ liệu cục bộ**: Đã được tải và tổ chức trong thư mục [`data/raw/`](data/raw/):
  - `data/raw/train.csv`: 16,738 mẫu (~22.3 MB)
  - `data/raw/dev.csv`: 2,090 mẫu (~2.8 MB)
  - `data/raw/test.csv`: 2,091 mẫu (~2.8 MB)
- **Nhãn kiểm chứng (3 nhãn cân bằng hoàn hảo)**:
  - `Supports`: Bằng chứng xác nhận phát biểu là đúng sự thật.
  - `Refutes`: Bằng chứng bác bỏ phát biểu (phát biểu sai sự thật).
  - `Not_Enough_Information`: Ngữ cảnh không đủ thông tin để khẳng định hay bác bỏ.

---

## 📂 Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
viet-factcheck/
├── data/
│   ├── raw/                                 # Dữ liệu gốc ViWikiFC từ Hugging Face
│   │   ├── train.csv                        # Tập huấn luyện (16,738 mẫu)
│   │   ├── dev.csv                          # Tập phát triển / validation (2,090 mẫu)
│   │   └── test.csv                         # Tập kiểm thử (2,091 mẫu)
│   └── processed/                           # Dữ liệu sau tiền xử lý / trích xuất đặc trưng
├── models/
│   └── checkpoints/                         # Thư mục lưu trữ trọng số mô hình đã huấn luyện
├── notebooks/
│   └── 01_exploratory_data_analysis.ipynb   # Notebook phân tích & trực quan hóa dữ liệu
├── docs/
│   ├── dataset_schema.md                    # Chi tiết lược đồ thuộc tính & phân phối nhãn
│   └── architecture.md                      # Sơ đồ luồng xử lý hệ thống (Retrieval -> Verification)
├── logs/                                    # Thư mục ghi log huấn luyện & thử nghiệm
├── src/
│   ├── __init__.py
│   ├── data/                                # Module xử lý dữ liệu và PyTorch Dataset
│   │   ├── __init__.py
│   │   └── dataset.py                       # ViWikiFCDataset, create_dataloader
│   ├── retrieval/                           # Module truy xuất bằng chứng
│   │   ├── __init__.py
│   │   └── bm25_retriever.py                # BM25 baseline retriever
│   ├── models/                              # Khối mô hình phân loại NLI / Fact-Checking
│   │   ├── __init__.py
│   │   └── classifier.py                    # FactCheckClassifier (InfoXLM / XLM-RoBERTa / PhoBERT)
│   ├── utils/                               # Các hàm bổ trợ
│   │   ├── __init__.py
│   │   ├── text_utils.py                    # Chuẩn hóa văn bản tiếng Việt
│   │   └── metrics.py                       # Đo lường đánh giá (Accuracy, Macro F1)
│   ├── train.py                             # Script huấn luyện mô hình
│   └── infer.py                             # Script dự đoán kiểm chứng phát biểu
├── .gitignore                               # Bỏ qua các file nhị phân nặng, checkpoint, log
├── requirements.txt                         # Danh sách thư viện cần thiết
└── README.md                                # Tài liệu tổng quan dự án
```

---

## ⚙️ Cài Đặt & Môi Trường

### Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Phân tích Dữ liệu (EDA)
Khám phá và trực quan hóa phân phối nhãn, độ dài văn bản qua Jupyter Notebook:
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

### 2. Huấn luyện Mô hình (Training)
Chạy script huấn luyện mô hình phân loại (mặc định dùng `xlm-roberta-base`, có thể đổi sang `vinai/phobert-base-v2` hoặc `microsoft/infoxlm-large`):
```bash
python -m src.train --model_name xlm-roberta-base --train_path data/raw/train.csv --dev_path data/raw/dev.csv --output_dir models/checkpoints/best_model --batch_size 16 --epochs 3 --lr 2e-5
```

### 3. Suy Luận & Kiểm Chứng Phát Biểu (Inference)
Dự đoán tính đúng/sai của phát biểu dựa trên câu bằng chứng đối soát:
```bash
python -m src.infer --model_dir models/checkpoints/best_model --claim "Chiến tranh với Campuchia đã kết thúc trước khi Việt Nam thống nhất." --evidence "Sau khi thống nhất, Việt Nam tiếp tục gặp khó khăn do các lệnh cấm vận và chiến tranh với Campuchia."
```

---

## 📑 Trích Dẫn (Citations)

Nếu sử dụng tài nguyên này trong nghiên cứu hoặc đề tài, vui lòng trích dẫn bài báo gốc của nhóm tác giả ViWikiFC:

```bibtex
@article{nguyen2024viwikifc,
  title   = {ViWikiFC: Fact-Checking for Vietnamese Wikipedia-Based Textual Knowledge Source},
  author  = {Nguyen, Nghiem T. and Vo, Nguyen-Khang and Nguyen, Kiet Van},
  journal = {arXiv preprint arXiv:2405.07615},
  year    = {2024},
  url     = {https://arxiv.org/abs/2405.07615}
}
```