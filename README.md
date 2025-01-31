# AutoRAG : Automatic RAG evaluation

## This implementation is based on the AutoRAG implementation [here](https://github.com/Marker-Inc-Korea/AutoRAG)

## Installation

```bash
conda env -f create dependencies/requirements.txt
```

## RAG Evaluation Dataset Creation

To use AutoRAG, you first need to create a RAG evaluation dataset. Follow the steps below to create and use the dataset yourself.

1. Run `minio_helper.py` to extract data from minIO (This is a custom step) and store under data/raw
```bash
python scripts/minio_helper.py --prefix static_crawler/processed/ --local_dir data/raw
```
2. Run `run_parse.py`. This file allows you to convert data/raw files to parquet file data/processed.
```bash
python scripts/run_parse.py --input_dir data/raw --output_path data/processed/combined.parquet
```
3. Execute `run_chunk.py` to perform chunking using various methods. You can check the chunking methods in `config/chunk.yaml`. You need to set the raw file at this point.
```bash
python scripts/run_chunk.py --raw_path ./data/processed/combined.parquet
```
5. After execution, check the `data/chunked_corpus` folder for the various chunked files created using different chunking methods.
6. Now, run the `make_qa.py` file. You need to set the raw file used for chunk creation and the chunk file to be used. Choose an appropriate chunk file, and you can generate a QA dataset using other chunk files later. You don't need to generate questions again. Refer to the update_corpus feature explained later.
```bash
python scripts/make_qa.py --raw_path ./data/processed/combined.parquet --corpus_path ./data/chunked_corpus/0.parquet --qa_size 100 --output_path ./data/QA/0.parquet --corpus_output_path ./data/corpus/0.parquet
```

## Running the Project Using main.py

1. Populate the .env file :
```bash
OPENAI_API_KEY=
LLAMA_CLOUD_API_KEY=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_ENDPOINT_URL=
AWS_BUCKET_NAME=
```
2. Run main.py as shown below to start AutoRAG.
```bash
python scripts/main.py --config ./config/main.yaml --qa_data_path data/QA/0.parquet --corpus_data_path data/corpus/0.parquet --project_dir benchmark
```
3. Once the benchmark folder is created, you can check the results there.


## Viewing the benchmark : Via dashboard

Run the command below to load the dashboard. You can easily review the results through the dashboard.

```bash
autorag dashboard --trial_dir ./benchmark/0
```

## Running Streamlit

Run Streamlit to directly use the optimized RAG. Execute the command below.

```bash
autorag run_web --trial_path ./benchmark/0
```
