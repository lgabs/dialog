# Dialog
This fork of Dialog is a Q&amp;A Chatbot Application with LLMs, using Langchain and LangServe. It is [LCEL first](https://python.langchain.com/docs/expression_language/), i.e., it follows the LangChain Expression Language design. It focus specifically on the problem of deploying a Q&A application that uses RAG for answers, i.e., one or more knowledge bases to augment the LLM's context. This can be achieved using langserve to serve any langchain's chain, which can include chat history and usually uses a vector store to store embeddings from the knowledge base and retriever to search for them. 

There are many ways of creating llm applications for a Q&A Chatbot, but not so trivial for beginners. The idea of this project is to present a default configuration for a production-ready chain, but allow customization in any component of the chain, including combination of chains.

Evaluation is also a very important part of LLM applications, and thereby dialog will also have support to evaluate your application easily.

Right now, this fork considers:
- for chat history: [Postgres](https://python.langchain.com/docs/integrations/memory/postgres_chat_message_history/)
- for vector store and retriever: [PGVector](https://python.langchain.com/docs/integrations/vectorstores/pgvector/)

We don't have a full documentation yet, but you will find the basic instructions to run this project in the [Get Started](#get-started) section below. Feel free to check the project issues, add your ideas, and also the [project's kanban](https://github.com/users/lgabs/projects/2).  

<blockquote style="background-color: #ffffcc; border-left: 10px solid #ffeb3b; padding: 15px;">
  <p><strong>Note:</strong> ❗ Important: this fork applies many breaking changes with the upstream original project. The main breaking changes is that we expose the application directly with langserve and delegates all processing to chains (or combination of chains)</p>
</blockquote>

## Get Started

To run it initially, download some example files to use as knowledge base. The `examples` folder contains some example files to run the application locally. To get an example of a Q&A dataset, download this [Question-Answer Dataset](https://www.kaggle.com/datasets/rtatman/questionanswer-dataset?resource=download&select=S08_question_answer_pairs.txt) into `examples/qa_example.csv` path and run `python examples/make_qa_example.py` to build a simple knowledge base with question and answer together (the result will be embedded together). Notice that this file does a simple processing and saves the csv to the `/data` folder. This is the default folder for the knowledge base. The default column to be embedded is called `Document`, all remaining columns will be added as metadata do the embedded document.

Then, run:
```
docker compose up
```

and you'll see two services running:
- `db` - the service for the postgres container (the same database is used for memory and vector store)
- `api` - the service to expose dialog api using langserve

Now, chat with dialog using the playground (at http://0.0.0.0:8080/chat/playground/) or access the api documentation at http://0.0.0.0:8080/docs, which includes all endpoints automatically created by langserve in the Swagger UI.


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
