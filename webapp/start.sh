#!/bin/bash
# Script to start Streamlit app

cd "$(dirname "$0")"
streamlit run app.py --server.port 8081 --server.address 0.0.0.0
