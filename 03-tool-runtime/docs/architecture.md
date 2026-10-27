# Architecture: Tool Runtime

The Tool Runtime separates business logic (tools) from authorization and generic argument validation.

```mermaid
flowchart TD
    A[Agent Application] -->|Requests Execution| E[ToolExecutor]
    E -->|1. Resolve Tool| R[ToolRegistry]
    R -->|Returns Definition & Handler| E
    E -->|2. Authorize| Auth[PermissionChecker]
    Auth -->|3. Success| E
    E -->|4. Validate Input| V[Pydantic Validation]
    V -->|5. Valid Arguments| H[ToolHandler]
    H -->|6. Execute side-effects| DB[(Business Systems)]
    H -->|7. Raw Data| E
    E -->|8. Validate Output| VO[Pydantic Validation]
    E -->|9. Structured Result| A
```

## Security Boundaries
1. **Identity & Tenant:** Tool arguments cannot override identity context. Identity is injected independently into the executor.
2. **Schema:** Inputs strictly bound to models. Unexpected arguments discarded or explicitly rejected.
3. **Registry:** LLM arbitrary function generation is impossible because LLMs simply pass a `tool_name` string, which the Registry resolves to an explicitly loaded callable.
