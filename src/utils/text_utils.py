"""Text processing utilities for Vietnamese text."""

import re
import unicodedata

def normalize_text(text: str) -> str:
    """Normalize unicode format (NFC) and clean whitespace."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_vietnamese_text(text: str, lower: bool = False) -> str:
    """Clean Vietnamese text for NLP tasks."""
    text = normalize_text(text)
    # Remove excessive punctuation repetitions
    text = re.sub(r"([!?.,;:]){2,}", r"\1", text)
    if lower:
        text = text.lower()
    return text
