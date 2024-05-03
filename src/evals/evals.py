import os
from typing import List, Dict
import json
from operator import itemgetter

import openai

from langsmith import Client
from langsmith.wrappers import wrap_openai
from langchain.smith import RunEvalConfig

from dialog.chains.rag import rag_chain

EVALS_PATH = os.environ["EVALS_PATH"]
DATASET_NAME = os.environ["DATASET_NAME"]


def read_openai_eval_examples(path: str) -> List[Dict]:
    """Parses evaluation samples when they are OpenAI's format for evals."""
    with open(path, "r") as jsonl_file:
        jsonl_list = list(jsonl_file)
    return [json.loads(jline) for jline in jsonl_list]


if __name__ == "__main__":
    # Choose a chain (making some input/output change to match with private eval sample)
    chain = (
        {"question": itemgetter("user_message")}
        | rag_chain
    )
    # Setup the evaluation
    client = Client()
    # Choose and LLM
    openai_client = wrap_openai(openai.Client())
    # Choose evaluators
    eval_config = RunEvalConfig(
        # We will use the chain-of-thought Q&A correctness as an example evaluator
        evaluators=["qa"],
    )
    results = client.run_on_dataset(
        dataset_name=DATASET_NAME, llm_or_chain_factory=chain, evaluation=eval_config
    )
    project_name = results["project_name"]
