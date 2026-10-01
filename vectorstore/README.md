# Vectorstore Directory

This folder holds persistent ChromaDB vector embeddings for the AI Travel Planner Agent.

Embeddings are built using `sentence-transformers/all-MiniLM-L6-v2` and contain indexed travel knowledge:
* Destination weather & best seasons
* Local cultural tips & etiquette
* Recommended local dishes and dining guides
* Packing checklists & travel hacks
* Common tourist scams to avoid
* Visa regulations & transit essentials

Vector storage databases (`*.sqlite3` and binary index files) are automatically ignored by git to avoid committing binary artifacts.
