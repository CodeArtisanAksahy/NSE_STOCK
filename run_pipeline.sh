#!/bin/bash

echo "Starting stock pipeline - $(date)"

# Step 1: Ingest data
cd ~/stock_pipeline
python3 ingest_stocks.py

# Step 2: Run dbt
cd ~/stock_pipeline/stock_pipeline
dbt run

echo "Pipeline completed - $(date)"
