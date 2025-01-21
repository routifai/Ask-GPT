import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llama_index.core import Settings
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader, PropertyGraphIndex
# Import settings
from utils.settings  import NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_URL, MD_FILES_DIRECTORY, PERSISTED_INDEXES_DIRECTORY


# Initialize LLM and embedding model
from utils.init import llm, embed_model
Settings.llm = llm
Settings.embed_model = embed_model

# Initialize Neo4j property graph store
graph_store = Neo4jPropertyGraphStore(
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    url=NEO4J_URL,
)

# Ensure required directories exist
os.makedirs(MD_FILES_DIRECTORY, exist_ok=True)
os.makedirs(PERSISTED_INDEXES_DIRECTORY, exist_ok=True)

# Load documents
documents = SimpleDirectoryReader(MD_FILES_DIRECTORY).load_data()

# Build the PropertyGraphIndex
index = PropertyGraphIndex.from_documents(
    documents,
    embed_model=embed_model,
    kg_extractors=[
        SchemaLLMPathExtractor(
            llm=llm
        )
    ],
    property_graph_store=graph_store,
    show_progress=True,
)

# Create a query engine
query_engine = index.as_query_engine(include_text=True)
