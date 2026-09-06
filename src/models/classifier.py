"""Fact Verification Classifier wrapper."""

import torch
import torch.nn as nn
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class FactCheckClassifier(nn.Module):
    """Sequence classification model wrapper for Fact Checking (3 classes)."""

    def __init__(self, model_name: str = "xlm-roberta-base", num_labels: int = 3):
        super().__init__()
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
        )

    def forward(self, input_ids, attention_mask, labels=None, **kwargs):
        return self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
            **kwargs,
        )

    def save_pretrained(self, save_dir: str):
        self.model.save_pretrained(save_dir)
