import os
from datetime import datetime
import pandas as pd
import click

@click.command()
@click.option('--input_dir', default="data/raw", help="Input directory containing markdown files")
@click.option('--output_path', default="data/processed/combined.parquet", help="Output Parquet file path")
def convert_to_parquet(input_dir: str,output_path: str):
    """
    Combine markdown files from a directory into a Parquet file
    """
    data = []
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Read all markdown files
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                data.append({
                    'texts': content,  # Content of the file
                    'path': file_path,  # Local path to the file
                    'page': 1,  # Set page to 1
                    'last_modified_datetime': current_datetime  # Current datetime
                })
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(data)

    # Save as Parquet
    df.to_parquet(output_path, engine='pyarrow')
    print(f"Parquet file saved to: {output_path}")


if __name__ == "__main__":
    convert_to_parquet()
