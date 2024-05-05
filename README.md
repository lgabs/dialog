# Dialog

This fork of Dialog is a Q&amp;A Chatbot Application with LLMs, using Langchain and LangServe. It is [LCEL first](https://python.langchain.com/docs/expression_language/), i.e., it follows the LangChain Expression Language design. It focus specifically on the problem of deploying a Q&A application that uses RAG for answers, i.e., one or more knowledge bases to augment the LLM's context. This can be achieved using langserve to serve any langchain's chain, which can include chat history and usually uses a vector store to store embeddings from the knowledge base and retriever to search for them. 

There are many ways of creating llm applications for a Q&A Chatbot, but not so trivial for beginners. The idea of this project is to present a default configuration for a production-ready chain, but allow customization in any component of the chain, including combination of chains.

Evaluation is also a very important part of LLM applications, and thereby dialog will also have support to evaluate your application easily.

Right now, this fork considers:
- for chat history: [Postgres](https://python.langchain.com/docs/integrations/memory/postgres_chat_message_history/)
- for vector store and retriever: [PGVector](https://python.langchain.com/docs/integrations/vectorstores/pgvector/)

We don't have a full documentation yet, but you will find the basic instructions to run this project in the [Get Started](#get-started) section below. Feel free to check the project issues, add your ideas, and also the [project's kanban](https://github.com/users/lgabs/projects/2).

<blockquote style="background-color: #ffffcc; border-left: 10px solid #ffeb3b; padding: 15px;">
  <p><strong>Note:</strong> ‼️ Important ‼️: this fork applies many breaking changes with the upstream original project, but which I see are beneficial for the project catch-up with langchain's framework. The main breaking changes is that we expose the application directly with langserve and delegates all processing to chains (or combination of chains). I hope that the ideas from this fork can foster constributions for the original repo 🙏. Also, this fork is not yet stable and can suffer breaking changes itself, since we're experimenting many things. </p>
</blockquote>

## How the solution works

If you are new to RAG tecnique for LLM applications like Q&A, check [langchain's documentation](https://python.langchain.com/docs/use_cases/question_answering/) on that. The solution basically follows the idea that LLMs can learn knowledge in two ways: 
- via model weights (i.e., fine-tune the model on a training set)
- via model inputs (i.e., insert the knowledge into an input message, via prompt)

The latter is usually more suitable to make a more reliable model for factual recall, and serves as a "short-memory", easier to recall, while the fine-tuning are like a long-term memory, difficult to recall. Check this nice [OpenAI cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb) for a deeper understanding.

Tipically, the architecture is like this:
- **indexing**: store knowledge in a "searchable" way into some store (in-memory or persistent). This is usually done with embeddings-based search, i.e., representing text with vectors.
- **RAG Chain**: build a chain that takes the user query (question) in runtime, searches for relevant data in the index, and include them in the prompt passed to the LLM.

With the chain created (or combination of chains), you can easly expose them as REST APIs with Langserve, and also monitor chain calls with Langsmith (check [this quickstart](https://docs.smith.langchain.com/hub/quickstart) and see the `.env.sample`). Both are parts of the Langchain's framework (more details [here](https://python.langchain.com/docs/get_started/introduction/#get-started)).

## Get Started

Before starting the dockerized application, you'll need a `.env` for environment variables; use the [`.env.sample`](https://github.com/lgabs/dialog/blob/main/.env.sample) as an example. It shows several variables and paths to the knowledge base and chain parameters. The `/data` folder is intentionally not versioned since they contain proprietary information.

To run it initially, use example files from `examples` folder (copy them to `/data` as shown in the `.env.sample`): 
- `examples/knowledge_base.csv`: a sample knowledge base from a [Kaggle dataset](https://www.kaggle.com/datasets/rtatman/questionanswer-dataset?resource=download&select=S08_question_answer_pairs.txt) about Abraham Lincoln. The default column to be embedded is `Document`, all remaining columns will be added as metadata do the embedded document.
- `examples/params`: toml files that stores chain parameters, like prompts and model's parameters, one file for each chain. These are used in runtime to compile the chains.

Then, run
```
docker compose up
```

and you'll see two services running:
- `db` - the service for the postgres container (the same database is used for memory and vector store)
- `dialog` - the service to expose dialog api using langserve. When starting, this service first fires a `make-embeddings` service to resolve the indexing phase.

Now, chat with dialog either:
- using the playground (at http://0.0.0.0:8080/chat/playground/, which also shows intermediate steps of the chain)
- accessing the api documentation at http://0.0.0.0:8080/docs, which includes all endpoints automatically created by langserve in the Swagger UI. 

The `src/dialog/app/server.py` defines the FastAPI API, and the langchain's `add_routes` exposes any chain under a specified `path`.By default, it exposes the `rag_with_history_chain`, which lives in `src/dialog/chains/rag_with_history`. All chains should be defined in the `src/dialog/chains` module, and you can serve as many as you want using add_routes with other paths.

## Evaluate your Chains

To learn more about evaluation of LLM applications, check [this post](https://medium.com/data-science-at-microsoft/evaluating-llm-systems-metrics-challenges-and-best-practices-664ac25be7e5). To evaluate your chain(s) with langsmith, you can create a dataset of input/output examples (check the `/examples/evals_example.jsonl` example) and upload it to langsmith (or create one there directly in the UI). Then, update the dataset name in your `.env`, and then run `make evals`, which will run the default default evaluation suite over your dataset and log the results in your datasets's experiments in langsmith UI. Since every application will have different evaluation suites, you can customize your `src/evals/evals.py` for that. Check more about langsmith evaluation [here](https://docs.smith.langchain.com/evaluation/quickstart).

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
  - [LLM evaluation](https://medium.com/data-science-at-microsoft/evaluating-llm-systems-metrics-challenges-and-best-practices-664ac25be7e5)
- [Langsmith evaluation suite](https://docs.smith.langchain.com/evaluation/quickstart)