#!/bin/bash

echo "🔄 Starting LLaMA model setup..."

# Step 1: Download models
echo "⬇️  Pulling LLaMA models with Ollama..."
ollama pull llama3.2_latest
ollama pull llama3:latest
ollama pull tinyllama:latest

# Optional Step 2: Run each model once to confirm they're working
echo "✅ Testing models with a basic prompt..."
echo "Q: Hello?\nA:" | ollama run llama3.2:latest
echo "Q: Hello?\nA:" | ollama run llama3:latest
echo "Q: Hello?\nA:" | ollama run tinyllama:latest

echo "✅ All done and working!"
