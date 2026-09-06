"""Inference script for Fact-Checking prediction."""

import argparse
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.data.dataset import ID2LABEL

def main():
    parser = argparse.ArgumentParser(description="Predict verdict for a Claim given Evidence")
    parser.add_argument("--model_dir", type=str, default="models/checkpoints/best_model")
    parser.add_argument("--claim", type=str, required=True, help="Claim to verify")
    parser.add_argument("--evidence", type=str, required=True, help="Evidence sentence")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_dir)
    model.eval()

    inputs = tokenizer(
        args.claim,
        args.evidence,
        return_tensors="pt",
        truncation=True,
        max_length=256,
        padding=True,
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0]
        pred_id = int(torch.argmax(probs))

    verdict = ID2LABEL.get(pred_id, "Unknown")
    print(f"Claim: {args.claim}")
    print(f"Evidence: {args.evidence}")
    print(f"Predicted Verdict: {verdict} (Confidence: {probs[pred_id]:.4f})")
    print(f"Probabilities: Supports: {probs[0]:.4f} | Refutes: {probs[1]:.4f} | Not Enough Info: {probs[2]:.4f}")

if __name__ == "__main__":
    main()
