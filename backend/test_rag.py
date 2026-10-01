import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.rag.ingestion import ingest_travel_knowledge
from app.rag.retriever import retrieve_travel_knowledge, format_travel_context
from app.rag.vector_store import get_travel_collection


def test_rag():
    print("\n--- 3. Testing ChromaDB Vector RAG Pipeline ---")
    ingest_travel_knowledge(force_reindex=False)

    col = get_travel_collection()
    count = col.count()
    print(f"[OK] ChromaDB collection item count: {count}")
    assert count > 0, "No travel knowledge items indexed in ChromaDB"

    # Test semantic retrieval
    results = retrieve_travel_knowledge("beach water sports nightlife in Goa", destination="Goa", top_k=2)
    print(f"[OK] Retrieved {len(results)} chunks for Goa.")
    assert len(results) > 0, "Failed to retrieve relevant chunks"
    for r in results:
        print(f"   - Match score: {r['score']}, Category: {r['metadata'].get('category')}")

    context = format_travel_context(results)
    assert len(context) > 20, "Formatted context empty"
    print("[OK] Formatted prompt context successfully.")

    print(">>> ChromaDB Vector RAG Test Passed Successfully!\n")


if __name__ == "__main__":
    test_rag()
