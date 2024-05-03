#!/bin/bash

if [ "$REBUILD_VECTORDB" == "true" ]; then
    echo "Running make_embeddings.py"
    python dialog/make_embeddings.py
else
    echo "Skipping make_embeddings.py"
fi

python evals/evals.py