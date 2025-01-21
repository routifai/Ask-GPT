import os
import sys
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
import nest_asyncio
import pandas as pd
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
    StorageContext,
    Settings,
)
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.node_parser import SimpleNodeParser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
nest_asyncio.apply()
from utils.settings import MD_FILES_DIRECTORY, PERSISTED_INDEXES_DIRECTORY, CSV_FILE_PATH
from utils.settings import initialize_settings

initialize_settings()

# Global caches for engines
SUBQUERY_ENGINE = None
PANDAS_QUERY_ENGINE = None

# Initialize the SimpleChatEngine
chat_engine = SimpleChatEngine.from_defaults(llm=Settings.llm)


def get_first_1000_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    tokens = text.split()
    return " ".join(tokens[:1000])


def generate_description_with_chat_engine(content):
    query = (
        f"Summarize the following content to create a concise description of the content of a file in less than 10 words:\n\n{content}"
    )
    response = chat_engine.chat(query)
    return response


def build_description_for_document_dynamic(file_path):
    content_snippet = get_first_1000_tokens(file_path)
    return generate_description_with_chat_engine(content_snippet)


def get_md_file_list(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.md')]


def process_markdown_files(md_files_directory, persisted_indexes_directory):
    query_engine_tools = []
    md_files = get_md_file_list(md_files_directory)

    for md_file in md_files:
        file_name_without_extension = os.path.splitext(os.path.basename(md_file))[0]
        document_persist_dir = os.path.join(persisted_indexes_directory, file_name_without_extension)

        if os.path.exists(document_persist_dir):
            print(f"Loading persisted index for {file_name_without_extension}...")
            storage_context = StorageContext.from_defaults(persist_dir=document_persist_dir)
            index = load_index_from_storage(storage_context, index_id=file_name_without_extension)
        else:
            print(f"Creating and persisting index for {file_name_without_extension}...")
            reader = SimpleDirectoryReader(input_files=[md_file])
            documents = reader.load_data()
            node_parser = SimpleNodeParser.from_defaults(chunk_size=1024)
            base_nodes = node_parser.get_nodes_from_documents(documents)
            index = VectorStoreIndex(base_nodes)
            index.set_index_id(file_name_without_extension)
            index.storage_context.persist(persist_dir=document_persist_dir)

        query_engine = index.as_query_engine()
        query_engine_tools.append(QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name=os.path.basename(md_file),
                description=str(build_description_for_document_dynamic(md_file))
            )
        ))
    return query_engine_tools


def initialize_subquery_engine(md_files_directory, persisted_indexes_directory, csv_file_path):
    global SUBQUERY_ENGINE
    if SUBQUERY_ENGINE is not None:
        print("Reusing cached SubQuestionQueryEngine...")
        return SUBQUERY_ENGINE

    query_engine_tools = process_markdown_files(md_files_directory, persisted_indexes_directory)
    csv_tool = process_csv_file(csv_file_path)
    if csv_tool:
        query_engine_tools.append(csv_tool)

    SUBQUERY_ENGINE = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=query_engine_tools,
        use_async=True,
        verbose=True
    )
    return SUBQUERY_ENGINE


def process_csv_file(csv_file_path):
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found at {csv_file_path}. Skipping PandasQueryEngine setup.")
        return None

    print("Loading CSV data into PandasQueryEngine...")
    df = pd.read_csv(csv_file_path)
    return QueryEngineTool(
        query_engine=PandasQueryEngine(df=df, verbose=True),
        metadata=ToolMetadata(
            name="Tax Data CSV",
            description="A csv containing tax-related information for querying."
        )
    )


def pandas_engine(csv_file_path):
    global PANDAS_QUERY_ENGINE
    if PANDAS_QUERY_ENGINE is not None:
        print("Reusing cached PandasQueryEngine...")
        return PANDAS_QUERY_ENGINE

    if not os.path.exists(csv_file_path):
        print(f"CSV file not found at {csv_file_path}. Skipping PandasQueryEngine setup.")
        return None

    print("Loading CSV data into PandasQueryEngine...")
    df = pd.read_csv(csv_file_path)
    PANDAS_QUERY_ENGINE = PandasQueryEngine(df=df, verbose=True)
    return PANDAS_QUERY_ENGINE


def create_react_agent(sub_query_engine, pandas_query_engine):
    def subquery(query):
        return str(sub_query_engine.query(query))

    subquery_tool = FunctionTool.from_defaults(
        fn=subquery,
        name="comparative_analysis",
        description="This tool can answer any open question about tax.",
    )

    def pandasquery(query):
        return str(pandas_query_engine.query(query))

    tax_data_csv_tool = FunctionTool.from_defaults(
        fn=pandasquery,
        name="tax_data_csv",
        description="This tool has access to tax data CSV, so any quantitative question can be answered by it.",
    )

    return ReActAgent.from_tools([tax_data_csv_tool, subquery_tool], verbose=True)


def initialize_react_agent(md_files_directory, persisted_indexes_directory, csv_file_path):
    sub_query_engine = initialize_subquery_engine(md_files_directory, persisted_indexes_directory, csv_file_path)
    pandas_query_engine = pandas_engine(csv_file_path)
    if pandas_query_engine is None:
        raise ValueError("Error: PandasQueryEngine not initialized because the CSV file was not found.")
    return create_react_agent(sub_query_engine, pandas_query_engine)


def main():
    try:
        react_agent = initialize_react_agent(
            MD_FILES_DIRECTORY, PERSISTED_INDEXES_DIRECTORY, CSV_FILE_PATH
        )
    except ValueError as e:
        print(f"Initialization Error: {e}")
        return

    test_queries = ["What are the filing requirements for Form 1040?"]

    for query in test_queries:
        print(f"\nQuery: {query}")
        response = react_agent.chat(query)
        print(f"Response: {response.response}")


if __name__ == "__main__":
    main()
