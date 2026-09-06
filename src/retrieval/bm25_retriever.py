"""BM25 baseline retriever for sentence / evidence candidate ranking."""

from typing import List, Tuple
from rank_bm25 import BM25Okapi

class BM25Retriever:
    """BM25 Evidence Retriever using sentence tokenization."""

    def __init__(self, corpus: List[str]):
        self.corpus = corpus
        self.tokenized_corpus = [doc.lower().split() for doc in corpus]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Retrieve top-k relevant candidate sentences for a given query/claim."""
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [(self.corpus[i], float(scores[i])) for i in top_indices]
