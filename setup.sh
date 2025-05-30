# Run flashcards pipeline
PYTHONPATH=./src python3 src/backend/flashcards_pipeline.py
echo "flashcards pipeline executed!"

# Run knowledge base pipeline
PYTHONPATH=./src python3 src/backend/knowledge_base_pipeline.py
echo "knowledge pipeline executed!"

# Run another script if needed
# python -m src.backend.other_module

echo "All pipelines completed!"
