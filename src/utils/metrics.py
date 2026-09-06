"""Evaluation metrics for Fact Verification."""

from typing import Dict
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_classification_metrics(preds: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
    """Compute accuracy, macro precision, recall, and F1."""
    acc = accuracy_score(labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="macro", zero_division=0
    )
    return {
        "accuracy": float(acc),
        "macro_precision": float(precision),
        "macro_recall": float(recall),
        "macro_f1": float(f1),
    }
