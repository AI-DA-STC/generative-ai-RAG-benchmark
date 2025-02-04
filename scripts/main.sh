#!/bin/bash

for i in {2..7}; do
    echo "Processing file $i of 7..."
    
    # Run make_qa.py
    echo "Running make_qa.py for file $i..."
    python scripts/make_qa.py \
        --raw_path ./data/processed/combined.parquet \
        --corpus_path "./data/chunked_corpus/$i.parquet" \
        --qa_size 100 \
        --output_path "./data/QA/$i.parquet" \
        --corpus_output_path "./data/corpus/$i.parquet"
    
    # Check if make_qa.py was successful
    if [ $? -ne 0 ]; then
        echo "Error: make_qa.py failed for file $i"
        exit 1
    fi
    
    # Run main.py
    echo "Running main.py for file $i..."
    python scripts/main.py \
        --config ./config/main.yaml \
        --qa_data_path "./data/QA/$i.parquet" \
        --corpus_data_path "./data/corpus/$i.parquet" \
        --project_dir benchmark_$i
    
    # Check if main.py was successful
    if [ $? -ne 0 ]; then
        echo "Error: main.py failed for file $i"
        exit 1
    fi
    
    echo "Successfully processed file $i"
done

echo "All files processed successfully!"