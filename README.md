
# SubQuery and ReACT Agent Solution: A Technical Overview

## Project Overview
This project implements a sophisticated pipeline to process, analyze, and query diverse document formats effectively. Our primary focus was building a robust framework that:

1. Ingests documents like PDFs, PowerPoint presentations, and Markdown files.
2. Leverages the capabilities of large language models (LLMs) to dynamically extract metadata, summarize content, and enable precise query resolution.
3. Utilizes advanced reasoning techniques to break down complex questions into manageable subqueries, ensuring high accuracy and relevance in answers.
4. Employs ReACT agents to dynamically choose the most appropriate tools for query resolution.
5. Benchmarks the system with a test set and LLM-based scoring to ensure precision and reliability.

---

## Key Features and Technical Implementation

### 1. **PDF to Markdown Conversion**
   - **Challenge:** PDFs often present data in unstructured formats, reducing model accuracy.
   - **Solution:** We implemented a robust pipeline to convert PDFs into Markdown format, improving tokenization and model interpretability. This aligns with recent studies demonstrating that Markdown-based ingestion increases LLM accuracy.

### 2. **PowerPoint to Markdown Transformation**
   - **Challenge:** Extracting meaningful content from slides requires handling text, visuals, and layouts.
   - **Solution:** By integrating LLM vision capabilities, we dynamically transform PowerPoint slides into Markdown, enabling accurate ingestion of slide content while preserving hierarchical information.

### 3. **Dynamic Metadata Extraction**
   - **Challenge:** Accurate metadata is critical for selecting the right tools for query resolution.
   - **Solution:** We implemented dynamic metadata extraction that identifies key attributes (e.g., topics, file types, and sections) to ensure the appropriate tool is selected for each query.

### 4. **SubQuery Engine**
   - **Challenge:** Addressing complex queries that require reasoning across multiple data sources.
   - **Solution:** A subquery engine breaks down intricate questions into smaller, interrelated questions (akin to a chain-of-thought process). This guided reasoning enables the system to iteratively "walk" through the problem space to derive accurate answers.

### 5. **ReACT Agent**
   - **Challenge:** Dynamically deciding the most appropriate tool to use for a query.
   - **Solution:** A ReACT agent evaluates the metadata and context to select between the subquery engine, PandasQueryEngine, or other tools, ensuring efficiency and precision.

### 6. **Benchmarking and Evaluation**
   - **Challenge:** Ensuring high precision and reliability in query results.
   - **Solution:**
     - We generated a custom test set with expected answers.
     - An LLM judge scored the system’s performance by comparing generated answers against the expected results.
     - This process provided a quantitative measure of the system’s accuracy and areas for improvement.

---

## Areas for Improvement
While the current implementation is robust, there are several areas we could explore to enhance functionality:

### 1. **Better Embedding Architecture**
   - Incorporate OCR capabilities for improved handling of images and tables.
   - Use advanced document processing tools like `unstructured` to refine embeddings.

### 2. **Agentic Workflow Implementation**
   - Transition to a more structured agent workflow using tools like LangGraph or LlamaIndex’s Workflows.

### 3. **Microservices Architecture**
   - Wrap the entire application into modular microservices using FastAPI to improve scalability and maintainability.

---

## Why This Solution Stands Out
1. **Complex Query Resolution:** Our subquery engine mirrors human-like reasoning by breaking down and sequentially resolving complex questions.
2. **Dynamic Tool Selection:** ReACT agent ensures seamless interaction between tools, optimizing for query type and data format.
3. **End-to-End Precision:** From ingestion to querying, each step has been fine-tuned for accuracy, as evidenced by benchmarking with a test set and LLM-based scoring.
4. **Future-Proof Design:** Despite time constraints, the architecture provides a solid foundation for future enhancements, including agentic workflows, better embeddings, and microservices deployment.

---

## Conclusion
This project showcases a technically sophisticated solution that bridges the gap between unstructured data and precise, actionable insights. While there is room for improvement, the current implementation successfully demonstrates the power of LLMs, dynamic metadata extraction, and advanced reasoning engines in modern document processing systems.

---

## Next Steps
- Implement OCR-based table and image processing.
- Transition to a microservices-based architecture.
- Explore agentic workflows for enhanced task orchestration.

Current Precision = 60%

## STEPS TO RUN THE PROJECT : (SET YOUR OPENAI API KEY under setting init.py)
pip install -r requirements.txt
- DATA INGESTION :
this will transform raw data to md files in processed folder 
python ingestion/ppt2md.py
python ingestion/pdf2md.py

- VectorQuery :
this will embed the md files and load them to in memory vec db with persist mode and init the ReAct agent 
python engines/vectorQueryEngine.py

- graphQueryEngine :

Docker Setup
To launch Neo4j locally, first ensure you have docker installed. Then, you can launch the database with the following docker command

docker run \
    -p 7474:7474 -p 7687:7687 \
    -v $PWD/data:/data -v $PWD/plugins:/plugins \
    --name neo4j-apoc \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4JLABS_PLUGINS=\[\"apoc\"\] \
    neo4j:latest
From here, you can open the db at http://localhost:7474/. On this page, you will be asked to sign in. Use the default username/password of neo4j and neo4j.

Once you login for the first time, you will be asked to change the password. setup your new password under utils/settings.py

this will embed the md files and load them to neo4j graph store and init the ReAct agent ( large pdf file can take time to process )
python engines/graphQueryEngine.py

- Benchmark :
python benchmark/test.py ( it will print after the run the precision score )