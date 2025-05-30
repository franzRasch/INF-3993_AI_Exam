#!/bin/bash

# Run flashcards pipeline
python -m src.backend.RAG.flashcards_pipeline
echo "flascards pipeline executed!"

# Run knowledge base pipeline
python -m src.backend.RAG.knowledge_base_pipeline
echo "knowledge pipeline executed!"

# Run another script if needed
# python -m src.backend.other_module

echo "All pipelines completed!"
