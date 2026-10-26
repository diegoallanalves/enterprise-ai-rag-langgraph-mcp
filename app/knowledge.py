"""Small deterministic retrieval baseline; replace with vector RAG in phase two."""
from dataclasses import dataclass
import re

DOCUMENTS = {
    "sla": "Service level agreements define response and resolution targets for incidents.",
    "data_quality": "Data quality checks include completeness, uniqueness, validity and freshness.",
    "rag": "Retrieval augmented generation grounds responses in retrieved documents.",
}

@dataclass(frozen=True)
class Hit:
    source: str
    content: str
    score: int


def retrieve(query: str, limit: int = 3) -> list[Hit]:
    tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
    hits = []
    for source, content in DOCUMENTS.items():
        searchable = set(re.findall(r"[a-z0-9]+", (source + " " + content).lower()))
        score = len(tokens & searchable)
        if score:
            hits.append(Hit(source, content, score))
    return sorted(hits, key=lambda h: (-h.score, h.source))[:limit]
