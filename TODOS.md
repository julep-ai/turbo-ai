- [ ] analytics: Add analytics
- [ ] embeddings: Add support for visualizing in nomic atlas
- [ ] misc: Add support for building chatgpt plugins
- [ ] turbo: add generic type information to @turbo decorator
- [ ] turbo: Add support for streaming
- [ ] turbo: Add an interactive chat runner .chat()
- [ ] debug: add visualizer
- [ ] docs_bot: create docs-bot to generate documentation
- [ ] misc: Add support for chaining
- [ ] misc: Decide nomenclature of what is an app, the factory function and a bot?
- [ ] bug: Fix user-type in default example for toolbot
- [ ] misc: Add support for embeddings
- [ ] turbo: hash-based deduplication of old history+new prompts
- [ ] random: change debug type -> source
- [ ] random: access memory and cache from outside
- [ ] turbo: simplify interface further
  + [ ] simplify: Remove Generate
  + [ ] simplify: generate after User
  + [ ] simplify: generated is sent back to yield site as Assistant() object
  + [ ] simplify: no more yielding Assistant
  + [ ] simplify: Rename GetInput to Input
  + [ ] simplify: Result exits app
  + [ ] simplify: If Input in a factory, it is an agent
  + [ ] simplify: .chat() for agents and .run() otherwise
  + [ ] simplify: Remove sticky messages
  + [ ] simplify: System messages go on top
  + [ ] simplify: Add key to identify
  + [ ] simplify: default key is hash + : + index
  + [ ] simplify: on re-run, memory + new messages are stacked together, new messages with the same key replace the previous, remaining are concatenated to prepare prompt
  + [ ] simplify: If key==None, then the message is used for generation and then immediately discarded without adding to memory
  + [ ] simplify: Add custom metadata to messages so `prepare_prompt` can use it for filtering etc
  + [ ] simplify: Add content_str as a stringified property getter
- [ ] implement turbo generator as a class implementation of async iterator instead of a proxied async_generator
- [x] debug: Add debug_color
- [x] debug: Make pygments and colorama optional deps under debug
- [x] turbo: Add support for n>1 choices and selection
- [x] turbo: Remove delay caused by tiktoken get_encoding by hardcoding stuff
- [x] turbo: Add support for args in addition to kwargs
- [x] perf: load encoding cached
- [x] cache: Add TTL support to RedisCache
- [x] misc: Add support for parsing completion outputs
- [x] cache: Add redis cache
- [x] scratchpad: Add support for parsing json lists in addition to objects
- [x] completion: dedent doc comment
- [x] fix: function docstring and signature getter
- [x] turbo: yield assistant ONLY on generate?
- [x] turbo: move memory_args and cache_args
- [x] tool_bot: use system/example everywhere but switch it to User prompt for gpt-3.5
- [x] tool_bot: additional_info should be added as a sticky top message
- [x] tool_bot: scratchpad cannot parse response that spans multiple lines
- [x] tool_bot: add infinite loop back
- [x] tool_bot: accept state and input as a dict
- [x] turbo: system should be sticky
