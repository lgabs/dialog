#!/bin/sh
uvicorn dialog.app.server:app --host $HOST --port $PORT