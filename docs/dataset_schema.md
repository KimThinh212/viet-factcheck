# ViWikiFC Dataset Schema & Overview

## 1. Source & Citation
- **Hugging Face Repository**: [High-Will/ViWikiFC](https://huggingface.co/datasets/High-Will/ViWikiFC)
- **Original Paper**: *ViWikiFC: Vietnamese Wikipedia Fact-Checking Dataset* ([arXiv:2405.07615](https://arxiv.org/abs/2405.07615))
- **Language**: Vietnamese (vi)
- **Domain**: Wikipedia-based Fact-Checking

## 2. Dataset Splits
| Split | Samples | Supports | Refutes | Not_Enough_Information | File Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | 16,738 | 5,594 | 5,573 | 5,571 | `data/raw/train.csv` |
| **Dev / Val** | 2,090 | 666 | 694 | 730 | `data/raw/dev.csv` |
| **Test** | 2,091 | 708 | 706 | 677 | `data/raw/test.csv` |
| **Total** | **20,919** | **6,968** | **6,973** | **6,978** | |

The dataset is exceptionally well-balanced across all three classes (approx. 33.3% per class).

## 3. Data Schema (Columns)

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `pairID` | String | Unique identifier for claim-evidence pair | `uit_424_27_39_3_11` |
| `sentenceID` | String | Unique identifier for the origin sentence | `uit_424_27_39_3` |
| `claim` | String | Fact-checking statement to be verified | `Ch? ?? qu?n ch? chuy?n ch? c?a nh? Thanh...` |
| `context` | String | Paragraph / text block extracted from Wikipedia | `Cu?i th?i nh? Thanh, do s? l?c h?u v?...` |
| `evidence` | String | Exact sentence in context used as verification ground | `Ch? ?? qu?n ch? chuy?n ch? ?? t? ra...` |
| `gold_label` | String | Ground-truth verdict: `Supports`, `Refutes`, `Not_Enough_Information` | `Supports` |
| `annotator_labels`| List / Str | Individual verdicts assigned by human annotators | `['Support']` |
| `title` | String | Title of the Wikipedia article | `Trung Qu?c` |
| `link` | String | Source URL of the Wikipedia article | `https://vi.wikipedia.org/Trung Qu?c` |

## 4. Task Definitions

1. **Evidence Retrieval (ER)**: Given a claim and context (or corpus), retrieve the most relevant evidence sentences.
2. **Verdict Classification (VC)**: Given a (Claim, Evidence) pair, classify into one of the 3 classes:
   - `Supports`: The evidence directly confirms the claim.
   - `Refutes`: The evidence contradicts the claim.
   - `Not_Enough_Information`: The evidence does not provide enough factual grounds to confirm or deny the claim.
3. **Full Fact-Checking Pipeline (ER + VC)**: End-to-end retrieval from raw text followed by verdict classification.
