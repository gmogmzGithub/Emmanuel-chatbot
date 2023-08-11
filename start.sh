#!/bin/sh
streamlit run src/Home.py --server.port=8501 --server.address=0.0.0.0 &
python src/server/webhook_server.py
