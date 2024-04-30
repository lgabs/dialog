# Dialog
This fork of Dialog is a Q&amp;A Application with LLMs, using Langchain and LangServe. It focus specifically on the problem of deploying a Q&A application that uses RAG for answers, i.e., a knowledge base to augment the LLM's context. This can be achieved using langserve to serve any langchain's chain, which can include chat history and usually uses a vector store to store embeddings from the knowledge base and retriever to search for them. The idea of this project is to present a default configuraion for a production-ready chain, but allow customization in any component of the chain, including combination of chains.

In this Right now, this fork considers:
- for chat history: [Postgres](https://python.langchain.com/docs/integrations/memory/postgres_chat_message_history/)
- for vector store and retriever: [PGVector](https://python.langchain.com/docs/integrations/vectorstores/pgvector/)

We don't have a full documentation yet, but you will find the basic instructions to run this project in the [Get Started](#get-started) section below.

<blockquote style="background-color: #ffffcc; border-left: 10px solid #ffeb3b; padding: 15px;">
  <p><strong>Note:</strong> ❗ ImportantThis fork applies many breaking changes with the upstream original project. The main breaking changes is that we expose the application directly with langserve and delegates all processing to chains (or combination of chains)</p>
</blockquote>

## Get Started

## TODOs/Ideas

I've already done some tasks, but I really think that the basic project structure should be with 
in-memory vectordb (and chat history too), since it's much easier to get started with and probably solves
many use cases that do not process too many documents or clients. Not all tasks should be done in sequence.

- [x] Update this readme with project idea and main components
- [x] Add docker compose with services for db (postgrest with pgvector) and api
- [x] Add memory (langchain_postgres package)
- [x] Add example dataset helpers for download
- [ ] use embedding id (useful to add or delete them by id in [pgvector](https://python.langchain.com/docs/integrations/vectorstores/pgvector/))
- [x] Add dataset (csv) loader and embedd into the vectordb
- [ ] Add retriever with pgvector
- [ ] Add use case or branch using in-memory vectordb/retriever and also in-memory chat history
- [ ] Add basic unit tests
- [ ] Add support to evaluate LLM answers (e.g [deepeval](https://github.com/confident-ai/deepeval) or [langsmith](https://docs.smith.langchain.com/evaluation) or [mlflow](https://mlflow.org/docs/latest/llms/llm-evaluate/index.html) evals, probably go for langsmith). Better to be some easy way of running them, and it'd good to add a workflow to allow eval in PRs.

# Example files

The `examples` folder contains some example files to run the application locally. To get an example of a Q&A dataset, download this [Question-Answer Dataset](https://www.kaggle.com/datasets/rtatman/questionanswer-dataset?resource=download&select=S08_question_answer_pairs.txt) into `examples/qa_example.csv` path and run `python examples/make_qa_example.py` to build a simple knowledge base with question and answer together (the result will be embedded together).

# References
- [LangChain Template - RAG Conversation](https://github.com/langchain-ai/langchain/tree/master/templates/rag-conversation)
- [Langchain Template - Chat with Persistence](https://github.com/langchain-ai/langserve/blob/main/examples/chat_with_persistence/server.py)
- [Langchain Conversation with Retrieval Chain](https://github.com/langchain-ai/langserve/blob/main/examples/conversational_retrieval_chain/server.py)
- [langchain-cli](https://github.com/langchain-ai/langchain/blob/master/libs/cli/DOCS.md)
