# Dialog

This fork of Dialog is a Q&amp;A Chatbot Application with LLMs, using Langchain and LangServe. It is [LCEL first](https://python.langchain.com/docs/expression_language/), i.e., it follows the LangChain Expression Language design. It focus specifically on the problem of deploying a Q&A application that uses RAG for answers, i.e., one or more knowledge bases to augment the LLM's context. This can be achieved using langserve to serve any langchain's chain, which can include chat history and usually uses a vector store to store embeddings from the knowledge base and retriever to search for them. 

There are many ways of creating llm applications for a Q&A Chatbot, but not so trivial for beginners. The idea of this project is to present a default configuration for a production-ready chain, but allow customization in any component of the chain, including combination of chains.

Evaluation is also a very important part of LLM applications, and thereby dialog will also have support to evaluate your application easily.

Right now, this fork considers:
- for chat history: [Postgres](https://python.langchain.com/docs/integrations/memory/postgres_chat_message_history/)
- for vector store and retriever: [PGVector](https://python.langchain.com/docs/integrations/vectorstores/pgvector/)

We don't have a full documentation yet, but you will find the basic instructions to run this project in the [Get Started](#get-started) section below. Feel free to check the project issues, add your ideas, and also the [project's kanban](https://github.com/users/lgabs/projects/2).

<blockquote style="background-color: #ffffcc; border-left: 10px solid #ffeb3b; padding: 15px;">
  <p><strong>Note:</strong> ‼️ Important ‼️: this fork applies many breaking changes with the upstream original project. The main breaking changes is that we expose the application directly with langserve and delegates all processing to chains (or combination of chains). I hope that the ideas from this fork can foster constributions for the original repo 🙏. Also, this fork is not yet stable and can suffer breaking changes itself, since we're experimenting many things. </p>
</blockquote>

## How the solution works

If you are new to RAG tecnique for LLM applications like Q&A, check [langchain's documentation](https://python.langchain.com/docs/use_cases/question_answering/) on that. The solution basically follows the idea that LLMs can learn knowledge in two ways: 
- via model weights (i.e., fine-tune the model on a training set)
- via model inputs (i.e., insert the knowledge into an input message, via prompt)

The latter is usually more suitable to make a more reliable model for factual recall, and serves as a "short-memory", easier to recall, while the fine-tuning are like a long-term memory, difficult to recall. Check this nice [OpenAI cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb) for a deeper understanding.

Tipically, the architecture is like this:
- **indexing**: store knowledge in a "searchable" way into some store (in-memory or persistent). This is usually done with embeddings-based search, i.e., representing text with vectors.
- **RAG Chain**: build a chain that takes the user query (question) in runtime, searches for relevant data in the index, and include them in the prompt passed to the LLM.

With the chain created (or combination of chains), you can easly expose them as REST APIs with Langserve, and also monitor chain calls with Langsmith. Both are parts of the Langchain's framework (more details [here](https://python.langchain.com/docs/get_started/introduction/#get-started)).

## Get Started

To run it initially, download this [Question-Answer Dataset](https://www.kaggle.com/datasets/rtatman/questionanswer-dataset?resource=download&select=S08_question_answer_pairs.txt) into `examples/qa_example.csv` path and run `python examples/make_qa_example.py` to build a simple knowledge base with question and answer together (the result will be embedded together). Notice that this file does a simple preprocessing and saves the csv to the `/data` folder. This is the default folder for the knowledge base. The default column to be embedded is called `Document`, all remaining columns will be added as metadata do the embedded document.

Before starting the dockerized application, you'll need a `.env` for environment variables; use the [`.env.sample`](https://github.com/lgabs/dialog/blob/main/.env.sample) as an example. After that, run:
```
docker compose up
```

and you'll see two services running:
- `db` - the service for the postgres container (the same database is used for memory and vector store)
- `api` - the service to expose dialog api using langserve

Now, chat with dialog using the playground (at http://0.0.0.0:8080/chat/playground/, which also shows intermediate steps of the chain) or access the api documentation at http://0.0.0.0:8080/docs, which includes all endpoints automatically created by langserve in the Swagger UI. 

The `src/dialog/app/server.py` defines the FastAPI API, and the langchain's `add_routes` exposes any chain under a specified `path`.By default, it exposes the `rag_with_history_chain`, which lives in `src/dialog/chains/rag_with_history`. All chains should be defined in the `src/dialog/chains` module, and you can serve as many as you want using add_routes with other paths.


## References
### Github project examples:
  - [LangChain Template - RAG Conversation](https://github.com/langchain-ai/langchain/tree/master/templates/rag-conversation)
  - [Langchain Template - Chat with Persistence](https://github.com/langchain-ai/langserve/blob/main/examples/chat_with_persistence/server.py)
  - [Langchain Conversation with Retrieval Chain](https://github.com/langchain-ai/langserve/blob/main/examples/conversational_retrieval_chain/server.py)
  - [langchain-cli](https://github.com/langchain-ai/langchain/blob/master/libs/cli/DOCS.md)
  - [langserve-launch-example](https://github.com/langchain-ai/langserve-launch-example)
### Documentations and blogposts:
  - Langchain's doc on [Q&A with RAG](https://python.langchain.com/docs/use_cases/question_answering/)
  - Langchain's [integrations for memory](https://python.langchain.com/docs/integrations/memory/) (postgres is [here](https://python.langchain.com/docs/integrations/memory/postgres_chat_message_history/))
  - Langchain's [integrations for vector stores](https://python.langchain.com/docs/integrations/vectorstores/) (pgvector is [here](https://python.langchain.com/docs/integrations/vectorstores/pgvector/))
