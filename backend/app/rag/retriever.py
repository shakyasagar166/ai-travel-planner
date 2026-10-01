import logging
from typing import List, Dict, Any, Optional
from app.rag.vector_store import get_travel_collection
from app.rag.embeddings import get_embeddings_model

logger = logging.getLogger(__name__)


def retrieve_travel_knowledge(
    query: str,
    destination: Optional[str] = None,
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Retrieves semantically relevant travel knowledge chunks from ChromaDB.
    """
    collection = get_travel_collection()
    if collection.count() == 0:
        return []

    embedder = get_embeddings_model()
    query_vector = embedder.embed_query(query)

    where_filter = None
    if destination:
        where_filter = {"destination": destination}

    try:
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, collection.count()),
            where=where_filter
        )
    except Exception as e:
        logger.warning(f"ChromaDB filtered query error ({e}), retrying without filter...")
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, collection.count())
        )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved = []
    for doc, meta, dist in zip(docs, metas, distances):
        retrieved.append({
            "text": doc,
            "metadata": meta,
            "score": round(1.0 - float(dist), 4) if dist is not None else 1.0
        })

    return retrieved


def format_travel_context(chunks: List[Dict[str, Any]]) -> str:
    """Formats retrieved chunks into clean markdown prompt context."""
    if not chunks:
        return "No specific archived travel guides found."
    lines = []
    for i, c in enumerate(chunks, 1):
        lines.append(f"[{i}] {c['text']}")
    return "\n".join(lines)
