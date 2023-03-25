[View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots)

The `turbo-chat` project provides various chatbot functionalities, such as question-answering, self-asking, subqueries handling, and text summarization. These functionalities are organized in separate modules and can be easily imported and used by other parts of the project.

For example, the `qa_bot` function in the `qa` module generates answers to questions based on a given context. It is an asynchronous function that uses a template string to format the input data and the `@turbo` decorator to control the generation process. Here's a sample usage:

```python
from turbo_chat import qa_bot

answer = qa_bot.ask("What is the capital of France?")
print(answer)
```

The `self_ask_bot` function in the `self_ask` module answers a given question step by step using a provided `qa_bot`. It generates sub-queries related to the main question and answers each sub-query before finally answering the main question. This approach allows the AI to break down complex questions into smaller parts. Here's an example:

```python
question = "How does photosynthesis work?"
context = "Photosynthesis is a process used by plants to convert sunlight into energy."
answer = await self_ask_bot(question, context, custom_qa_bot).run()
print(answer.content)
```

The `summarize_bot` function in the `summarize` module generates a summary of a given text using OpenAI's GPT-3.5 Turbo model. It is an asynchronous function that uses a template to format the input data. Here's a sample usage:

```python
import asyncio
from turbo_chat import summarize_bot

async def main():
    text = "This is a sample text that needs to be summarized."
    summary = await summarize_bot(text, text_type="text")
    print(summary)

asyncio.run(main())
```

The `subqueries_bot` functionality in the `subqueries` module decomposes a given request into a series of subqueries that can be used to query a knowledgebase. This is useful when a single question requires multiple pieces of information to provide a comprehensive answer. Here's an example:

```python
request = "What is the least expensive cereal that is healthy and has a low calorie content but is also tasty?"
context = "User is a customer at a grocery store and is asking the question to the store manager."

subqueries = await subqueries_bot(request, context)
print(subqueries)
```

The `tool_bot` functionality in the `tool` module handles user queries and provides responses using a set of tools. It is designed to work with the OpenAI GPT-3.5-turbo model. Here's an example of how the `tool_bot` function might be used:

```python
tools = [GetInformation, Calculate, Translate]
prologue = "Welcome to Turbo Chat!"
user_type = "customer"
instruction = "Ask me anything, and I'll try to help you using my available tools."

await tool_bot(tools, prologue, user_type, instruction)
```

These chatbot functionalities help keep the project organized and make it easier for developers to access and use the various chatbot functionalities provided by the `turbo-chat` project.
