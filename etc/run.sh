#!/bin/bash

if [ "$REBUILD_VECTORDB" == "true" ]; then
    echo "Running make_embeddings.py"
    python dialog/make_embeddings.py
else
    echo "Skipping make_embeddings.py"
fi

uvicorn dialog.app.server:app --host 0.0.0.0 --port 8080 --reload