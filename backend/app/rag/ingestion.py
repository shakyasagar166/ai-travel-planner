import json
import logging
import os
from app.rag.vector_store import get_travel_collection
from app.rag.embeddings import get_embeddings_model

logger = logging.getLogger(__name__)


def ingest_travel_knowledge(force_reindex: bool = False):
    """
    Ingests travel guides, weather, local tips, and safety advisories into ChromaDB.
    """
    collection = get_travel_collection()
    count = collection.count()

    if count > 0 and not force_reindex:
        logger.info(f"ChromaDB travel collection already contains {count} knowledge chunks. Skipping reindex.")
        return

    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    root_dir = os.path.dirname(backend_dir)
    possible_paths = [
        os.path.join(root_dir, "data", "destinations.json"),
        os.path.join(backend_dir, "data", "destinations.json"),
        os.path.join(os.getcwd(), "data", "destinations.json"),
    ]
    json_path = None
    for p in possible_paths:
        if os.path.exists(p):
            json_path = p
            break

    if not json_path:
        logger.warning(f"Knowledge file not found in possible locations: {possible_paths}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        destinations = json.load(f)

    embedder = get_embeddings_model()
    docs = []
    metadatas = []
    ids = []

    for d in destinations:
        dest_name = d["name"]
        city = d["city"]
        country = d["country"]

        # Chunk 1: Overview & Weather
        doc_1 = (
            f"Destination: {dest_name}, {country} ({city}). "
            f"Climate: {d.get('climate')}. Best Season to Visit: {d.get('best_season')}. "
            f"Average Daily Budget: ₹{d.get('avg_daily_budget_inr')}. "
            f"Overview: {d.get('description')} "
            f"Tags: {', '.join(d.get('tags', []))}."
        )
        docs.append(doc_1)
        metadatas.append({"destination": dest_name, "category": "overview", "city": city})
        ids.append(f"doc_{dest_name.lower()}_overview")

        # Chunk 2: Attractions & Activities
        attr_summaries = []
        for a in d.get("attractions", []):
            attr_summaries.append(
                f"{a['name']} ({a['category']}): {a['description']} "
                f"Entry fee: ₹{a['entry_fee_inr']}, Duration: {a['duration_hours']}h, "
                f"Rating: {a['rating']}/5, Best time: {a['best_time_of_day']}."
            )
        doc_2 = f"Attractions and Activities in {dest_name}: " + " | ".join(attr_summaries)
        docs.append(doc_2)
        metadatas.append({"destination": dest_name, "category": "attractions", "city": city})
        ids.append(f"doc_{dest_name.lower()}_attractions")

        # Chunk 3: Local Tips, Culture & Safety
        tips = d.get("travel_tips", [])
        doc_3 = (
            f"Travel Tips, Etiquette, Transport and Safety in {dest_name}: "
            + " ".join(tips)
        )
        docs.append(doc_3)
        metadatas.append({"destination": dest_name, "category": "tips", "city": city})
        ids.append(f"doc_{dest_name.lower()}_tips")

    logger.info(f"Computing embeddings for {len(docs)} travel knowledge documents...")
    embeddings = embedder.embed_documents(docs)

    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    logger.info(f"Successfully indexed {len(docs)} travel knowledge chunks into ChromaDB!")
