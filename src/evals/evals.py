import os
from typing import List, Dict
import json

import openai

from langsmith import Client
from langsmith.wrappers import wrap_openai
from langchain.smith import RunEvalConfig

from dialog.chains.rag_with_history import rag_with_history_chain

EVALS_PATH = os.environ["EVALS_PATH"]

def read_openai_eval_examples(path: str) -> List[Dict]:
    """Parses evaluation samples when they are OpenAI's format for evals."""
    with open(path, 'r') as jsonl_file:
        jsonl_list = list(jsonl_file)
    return [json.loads(jline) for jline in jsonl_list]


if __name__ == "__main__":
    # Choose a chain
    chain = rag_with_history_chain

    # Setup the evaluation
    client = Client()
    dataset_name = "Q&A samples"
    dataset = client.create_dataset(dataset_name, description="questions and answers.")
    samples = read_openai_eval_examples(EVALS_PATH)
    for sample in samples:
        client.create_examples(
            inputs={"question": sample["input"]},
            outputs={"answer": sample["ideal"]},
    dataset_id=dataset.id,
    )
    # Choose and LLM
    openai_client = wrap_openai(openai.Client())
    # Choose evaluators
    eval_config = RunEvalConfig(
        # We will use the chain-of-thought Q&A correctness evaluator
        evaluators=["qa"],
    )
    results = client.run_on_dataset(
    dataset_name=dataset_name, llm_or_chain_factory=chain, evaluation=eval_config
    )
    project_name = results["project_name"]
            
            