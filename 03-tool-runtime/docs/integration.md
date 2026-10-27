# Integration with Prior Projects

## With Project 1 (LLM Gateway)
The LLM Gateway issues model requests. If the model responds with a ToolCall request, the agent parses that request and forwards it to this `ToolExecutor`.

The `ToolRuntime` is agnostic to the LLM Gateway; it purely executes tools. You can format the resulting `ToolResult` into a tool response message via Project 1's `Message.tool()` method.

## With Project 2 (Prompt Engine)
The Tool Runtime's catalog of tools (including their descriptions and JSON schemas) can be injected into the Prompt Engine templates to instruct the model on what tools are available.

## Example Flow
See `examples/agent_tool_loop.py` for a conceptual integration.
