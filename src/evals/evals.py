import os
from typing import List, Dict
import json
from operator import itemgetter

import openai

from langsmith import Client
from langsmith.wrappers import wrap_openai
from langchain.smith import RunEvalConfig

from dialog.chains.rag import rag_chain

DATASET_NAME = os.environ["DATASET_NAME"]


if __name__ == "__main__":
    # Choose a chain (TODO: use 'question' for input key, this workaround is to test an existent dataset)
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
