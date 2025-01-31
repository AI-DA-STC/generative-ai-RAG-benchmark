import os

import click
from dotenv import load_dotenv

from autorag.chunker import Chunker

import pyprojroot
import sys
root = pyprojroot.find_root(pyprojroot.has_dir("config"))
sys.path.append(str(root))
from config import settings


@click.command()
@click.option('--raw_path', type=click.Path(exists=True, dir_okay=False, file_okay=True),
			  default=os.path.join(settings.BASE, "data/processed", "combined.parquet"))
@click.option('--config', type=click.Path(exists=True, dir_okay=False), default=os.path.join(settings.BASE, "config", "chunk.yaml"))
@click.option('--project_dir', type=click.Path(dir_okay=True), default=os.path.join(settings.BASE, "data/chunked_corpus"))
def main(raw_path, config, project_dir):
	load_dotenv()

	if not os.path.exists(project_dir):
		os.makedirs(project_dir)

	parser = Chunker.from_parquet(raw_path, project_dir=project_dir)
	parser.start_chunking(config)


if __name__ == '__main__':
	main()
