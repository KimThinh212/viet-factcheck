"""PyTorch Dataset module for ViWikiFC claim-evidence pairs."""

from typing import Optional, List, Dict
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import PreTrainedTokenizerBase

LABEL2ID = {
    "Supports": 0,
    "Refutes": 1,
    "Not_Enough_Information": 2,
}
ID2LABEL = {v: k for k, v in LABEL2ID.items()}

class ViWikiFCDataset(Dataset):
    """Dataset class for Vietnamese Fact-Checking."""

    def __init__(
        self,
        df: pd.DataFrame,
        tokenizer: PreTrainedTokenizerBase,
        max_length: int = 256,
        use_evidence: bool = True,
    ):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.use_evidence = use_evidence

        self.claims = df["claim"].fillna("").astype(str).tolist()
        if use_evidence and "evidence" in df.columns:
            self.contexts = df["evidence"].fillna("").astype(str).tolist()
        elif "context" in df.columns:
            self.contexts = df["context"].fillna("").astype(str).tolist()
        else:
            self.contexts = [""] * len(self.claims)

        if "gold_label" in df.columns:
            self.labels = [LABEL2ID.get(lbl, -1) for lbl in df["gold_label"]]
        else:
            self.labels = None

    def __len__(self) -> int:
        return len(self.claims)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        claim = self.claims[idx]
        context = self.contexts[idx]

        encoding = self.tokenizer(
            text=claim,
            text_pair=context,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )

        item = {k: v.squeeze(0) for k, v in encoding.items()}
        if self.labels is not None:
            item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

def create_dataloader(
    csv_path: str,
    tokenizer: PreTrainedTokenizerBase,
    batch_size: int = 16,
    max_length: int = 256,
    shuffle: bool = False,
    use_evidence: bool = True,
) -> DataLoader:
    df = pd.read_csv(csv_path)
    dataset = ViWikiFCDataset(df, tokenizer, max_length=max_length, use_evidence=use_evidence)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
