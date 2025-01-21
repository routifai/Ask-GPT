import os
from llama_index.core import Settings
from utils.init import llm, embed_model

# Initialize LLM and embedding model
Settings.llm = llm
Settings.embed_model = embed_model

# Directory paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MD_FILES_DIRECTORY = os.path.join(BASE_DIR, "/Users/simo/Sourcecode/Askme-GPT/data/taxgpt/processed")
PERSISTED_INDEXES_DIRECTORY = os.path.join(BASE_DIR, "/Users/simo/Sourcecode/Askme-GPT/data/taxgpt/persisted_indexes")
CSV_FILE_PATH = os.path.join(BASE_DIR, "/Users/simo/Sourcecode/Askme-GPT/data/taxgpt/raw/tax_data.csv")
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = ""
NEO4J_URL = "bolt://localhost:7687"

def initialize_settings():
    """Initialize any other global settings if required."""
    os.makedirs(MD_FILES_DIRECTORY, exist_ok=True)
    os.makedirs(PERSISTED_INDEXES_DIRECTORY, exist_ok=True)
