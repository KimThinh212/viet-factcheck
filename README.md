# Viet-Factcheck: Vietnamese Information Fact-Checking System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![HuggingFace Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-High--Will%2FViWikiFC-yellow)](https://huggingface.co/datasets/High-Will/ViWikiFC)
[![Paper](https://img.shields.io/badge/arXiv-2405.07615-b31b1b.svg)](https://arxiv.org/abs/2405.07615)

D? ?n **Viet-Factcheck** l? h? th?ng ki?m ch?ng t?nh x?c th?c c?a c?c ph?t bi?u (Fact-Checking / Claim Verification) d?a tr?n ngu?n tri th?c b?ch khoa to?n th? ti?ng Vi?t (Wikipedia). H? th?ng gi?i quy?t b?i to?n: ??i so?t m?t ph?t bi?u (`claim`), truy xu?t b?ng ch?ng ??i so?t (`evidence`) t? v?n b?n ng? c?nh (`context`), v? ph?n lo?i nh?n x?c th?c (`Supports`, `Refutes`, `Not_Enough_Information`).

---

## ?? Ngu?n D? Li?u (Dataset Attribution)

D? li?u ???c s? d?ng trong d? ?n n?y l? b? d? li?u g?c **ViWikiFC** (Vietnamese Wikipedia Fact-Checking Dataset):
- **Kho l?u tr? Hugging Face**: [High-Will/ViWikiFC](https://huggingface.co/datasets/High-Will/ViWikiFC)
- **T?c gi? & B?i b?o**: *ViWikiFC: Fact-Checking for Vietnamese Wikipedia-Based Textual Knowledge Source* ([arXiv:2405.07615](https://arxiv.org/abs/2405.07615)).
- **D? li?u c?c b?**: ?? ???c t?i v? l?u tr? trong th? m?c [`data/raw/`](data/raw/):
  - `data/raw/train.csv`: 16,738 m?u
  - `data/raw/dev.csv`: 2,090 m?u
  - `data/raw/test.csv`: 2,091 m?u
- **Nh?n ki?m ch?ng (3 nh?n c?n b?ng)**:
  - `Supports`: B?ng ch?ng x?c nh?n ph?t bi?u l? ??ng.
  - `Refutes`: B?ng ch?ng b?c b? ph?t bi?u.
  - `Not_Enough_Information`: Kh?ng ?? th?ng tin t? ng? c?nh ?? kh?ng ??nh hay b?c b?.

---

## ?? C?u Tr?c Th? M?c D? ?n (Project Structure)

```text
viet-factcheck/
??? data/
?   ??? raw/                       # D? li?u g?c ViWikiFC t? Hugging Face
?   ?   ??? train.csv              # T?p hu?n luy?n (16,738 m?u)
?   ?   ??? dev.csv                # T?p ph?t tri?n / validation (2,090 m?u)
?   ?   ??? test.csv               # T?p ki?m th? (2,091 m?u)
?   ??? processed/                 # D? li?u sau ti?n x? l? / tr?ch xu?t ??c tr?ng
??? models/
?   ??? checkpoints/               # Th? m?c l?u tr? tr?ng s? m? h?nh ?? hu?n luy?n
??? notebooks/
?   ??? 01_exploratory_data_analysis.ipynb # Notebook ph?n t?ch & tr?c quan h?a d? li?u
??? docs/
?   ??? dataset_schema.md          # Chi ti?t l??c ?? thu?c t?nh & ph?n ph?i nh?n
?   ??? architecture.md            # S? ?? lu?ng x? l? h? th?ng (Retrieval -> Verification)
??? logs/                          # Th? m?c ghi log hu?n luy?n & th? nghi?m
??? src/
?   ??? __init__.py
?   ??? data/                      # Module x? l? d? li?u v? PyTorch Dataset
?   ?   ??? __init__.py
?   ?   ??? dataset.py             # ViWikiFCDataset, create_dataloader
?   ??? retrieval/                 # Module truy xu?t b?ng ch?ng
?   ?   ??? __init__.py
?   ?   ??? bm25_retriever.py      # BM25 baseline retriever
?   ??? models/                    # Kh?i m? h?nh ph?n lo?i NLI / Fact-Checking
?   ?   ??? __init__.py
?   ?   ??? classifier.py          # FactCheckClassifier (InfoXLM / XLM-RoBERTa / PhoBERT)
?   ??? utils/                     # C?c h?m b? tr?
?   ?   ??? __init__.py
?   ?   ??? text_utils.py          # Chu?n h?a v?n b?n ti?ng Vi?t
?   ?   ??? metrics.py             # ?o l??ng ??nh gi? (Accuracy, Macro F1)
?   ??? train.py                   # Script hu?n luy?n m? h?nh
?   ??? infer.py                   # Script d? ?o?n ki?m ch?ng ph?t bi?u
??? .gitignore                     # B? qua c?c file nh? ph?n n?ng, checkpoint, log
??? requirements.txt               # Danh s?ch th? vi?n c?n thi?t
??? README.md                      # T?i li?u t?ng quan d? ?n
```

---

## ?? C?i ??t & M?i Tr??ng

### 1. C?i ??t c?c th? vi?n ph? thu?c:
```bash
pip install -r requirements.txt
```

---

## ?? H??ng D?n S? D?ng

### 1. Ph?n t?ch D? li?u (EDA)
M? notebook ph?n t?ch d? li?u tr?c quan:
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

### 2. Hu?n luy?n M? h?nh (Training)
Ch?y script hu?n luy?n m? h?nh ph?n lo?i (m?c ??nh d?ng `xlm-roberta-base`, c? th? ??i sang `microsoft/infoxlm-large` ho?c `vinai/phobert-base-v2`):
```bash
python -m src.train \
    --model_name xlm-roberta-base \
    --train_path data/raw/train.csv \
    --dev_path data/raw/dev.csv \
    --output_dir models/checkpoints/best_model \
    --batch_size 16 \
    --epochs 3 \
    --lr 2e-5
```

### 3. Suy Lu?n & Ki?m Ch?ng Ph?t Bi?u (Inference)
D? ?o?n t?nh ??ng/sai c?a ph?t bi?u d?a tr?n b?ng ch?ng:
```bash
python -m src.infer \
    --model_dir models/checkpoints/best_model \
    --claim "Chi?n tranh v?i Campuchia ?? k?t th?c tr??c khi Vi?t Nam th?ng nh?t." \
    --evidence "Sau khi th?ng nh?t, Vi?t Nam ti?p t?c g?p kh? kh?n do c?c l?nh c?m v?n v? chi?n tranh v?i Campuchia."
```

---

## ?? T?i Li?u Tham Kh?o (Citations)

N?u s? d?ng t?i nguy?n n?y, vui l?ng tr?ch d?n b?i b?o g?c c?a t?c gi? ViWikiFC:

```bibtex
@article{nguyen2024viwikifc,
  title   = {ViWikiFC: Fact-Checking for Vietnamese Wikipedia-Based Textual Knowledge Source},
  author  = {Nguyen, Nghiem T. and Vo, Nguyen-Khang and Nguyen, Kiet Van},
  journal = {arXiv preprint arXiv:2405.07615},
  year    = {2024},
  url     = {https://arxiv.org/abs/2405.07615}
}
```
