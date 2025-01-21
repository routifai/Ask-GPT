import os
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Set the API key directly in the code
os.environ["OPENAI_API_KEY"] = ""
# Retrieve the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI LLM
llm = OpenAI(
    model="gpt-4o-mini",
    api_key=api_key,
    max_tokens=500,
    temperature=0.3
)

# Initialize the embedding model
embed_model = OpenAIEmbedding(
    model_name="text-embedding-3-small",
    api_key=api_key
)
