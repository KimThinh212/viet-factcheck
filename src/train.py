"""Training script for Vietnamese Fact-Checking on ViWikiFC."""

import argparse
import os
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AdamW, get_linear_schedule_with_warmup
from tqdm import tqdm
import numpy as np

from src.data.dataset import create_dataloader, LABEL2ID, ID2LABEL
from src.models.classifier import FactCheckClassifier
from src.utils.metrics import compute_classification_metrics

def parse_args():
    parser = argparse.ArgumentParser(description="Train Fact-Checking Classifier on ViWikiFC")
    parser.add_argument("--model_name", type=str, default="xlm-roberta-base", help="Pretrained HF model")
    parser.add_argument("--train_path", type=str, default="data/raw/train.csv", help="Path to train CSV")
    parser.add_argument("--dev_path", type=str, default="data/raw/dev.csv", help="Path to dev CSV")
    parser.add_argument("--output_dir", type=str, default="models/checkpoints/best_model", help="Save directory")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--max_length", type=int, default=256, help="Max sequence length")
    return parser.parse_args()

def main():
    args = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    train_loader = create_dataloader(
        args.train_path, tokenizer, batch_size=args.batch_size, max_length=args.max_length, shuffle=True
    )
    dev_loader = create_dataloader(
        args.dev_path, tokenizer, batch_size=args.batch_size, max_length=args.max_length, shuffle=False
    )

    model = FactCheckClassifier(args.model_name, num_labels=len(LABEL2ID))
    model.to(device)

    optimizer = AdamW(model.parameters(), lr=args.lr)
    total_steps = len(train_loader) * args.epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=int(total_steps * 0.1), num_training_steps=total_steps)

    best_f1 = 0.0
    os.makedirs(args.output_dir, exist_ok=True)

    for epoch in range(args.epochs):
        model.train()
        total_loss = 0.0
        loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{args.epochs} [Train]")
        for batch in loop:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            scheduler.step()

            total_loss += loss.item()
            loop.set_postfix(loss=loss.item())

        # Evaluate on Dev set
        model.eval()
        all_preds, all_labels = [], []
        with torch.no_grad():
            for batch in tqdm(dev_loader, desc=f"Epoch {epoch+1}/{args.epochs} [Val]"):
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)

                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
                all_preds.extend(preds)
                all_labels.extend(labels.cpu().numpy())

        metrics = compute_classification_metrics(np.array(all_preds), np.array(all_labels))
        print(f"Validation Metrics: Acc: {metrics['accuracy']:.4f} | Macro F1: {metrics['macro_f1']:.4f}")

        if metrics["macro_f1"] > best_f1:
            best_f1 = metrics["macro_f1"]
            model.save_pretrained(args.output_dir)
            tokenizer.save_pretrained(args.output_dir)
            print(f"Saved best model with Macro F1: {best_f1:.4f} to {args.output_dir}")

if __name__ == "__main__":
    main()
