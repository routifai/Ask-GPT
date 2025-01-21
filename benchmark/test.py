import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from utils.settings import MD_FILES_DIRECTORY, PERSISTED_INDEXES_DIRECTORY, CSV_FILE_PATH
from llama_index.core.chat_engine import SimpleChatEngine
from utils.settings import initialize_settings
from llama_index.core import Settings
from engines.vectorQueryEngine import initialize_react_agent
from utils.init import llm
Settings.llm=llm
initialize_settings()

# Initialize LLM-based evaluation engine
evaluation_chat_engine = SimpleChatEngine.from_defaults()
react_agent = initialize_react_agent(
            MD_FILES_DIRECTORY, PERSISTED_INDEXES_DIRECTORY, CSV_FILE_PATH
        )
def evaluate_answer_llm(question, predicted_answer, expected_answer):
    """
    Uses an LLM to evaluate the quality of the predicted answer.
    Returns True if the predicted answer is evaluated as correct, otherwise False.
    """
    query = f"""
    Evaluate the following question and answers:
    Question: {question}
    Predicted Answer: {predicted_answer}
    Expected Answer: {expected_answer}
    
   Determine whether the predicted answer is correct or sufficiently similar to the expected answer.
   if the answer is a number if it approximately equal to predicted answer consider it true 
   Consider the predicted answer as correct if it aligns in meaning, even if it includes more or fewer details.
   Otherwise, consider it incorrect. Respond with 'True' for correct and 'False' for incorrect.
   """
    response = evaluation_chat_engine.chat(query).response
    return response.lower() == "true"


def benchmark_subquery_engine(sub_query_engine, test_data):
    """
    Benchmarks the subquery engine against a test dataset.
    Returns precision and recall along with detailed results.
    """
    results = []
    correct_predictions = 0
    total_questions = len(test_data)

    for _, row in test_data.iterrows():
        question = row["Query"]
        expected_answer = row["Expected Answer"]

        # Get the predicted answer from the subquery engine
        print(f"question ===>{question}")
        predicted_answer = sub_query_engine.query(question).response
        print(f"answer ====>{predicted_answer}")

        # Evaluate the predicted answer using the LLM
        is_correct = evaluate_answer_llm(question, predicted_answer, expected_answer)

        results.append({
            "Question": question,
            "Expected Answer": expected_answer,
            "Predicted Answer": predicted_answer,
            "Is Correct": is_correct
        })

        # Count correct predictions
        if is_correct:
            correct_predictions += 1

    # Calculate precision and recall
    precision = correct_predictions / total_questions if total_questions > 0 else 0
    recall = precision  # Precision and recall are equivalent in this context

    return precision, recall, pd.DataFrame(results)


def main():
    # Initialize the subquery engine
    sub_query_engine = initialize_react_agent(
        MD_FILES_DIRECTORY, PERSISTED_INDEXES_DIRECTORY, CSV_FILE_PATH
    )

    # Load test data
    test_data_path = "/Users/simo/Sourcecode/AskMe/benchmark/test_data.csv"  # Update with the actual path to the test dataset
    test_data = pd.read_csv(test_data_path)

    # Benchmark the engine
    precision, recall, results_df = benchmark_subquery_engine(sub_query_engine, test_data)

    # Output results
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")

    # Save detailed results to a file
    results_df.to_csv("/Users/simo/Sourcecode/AskMe/benchmark/evaluation_results.csv", index=False)
    print("Detailed results saved to 'evaluation_results.csv'.")


if __name__ == "__main__":
    main()
