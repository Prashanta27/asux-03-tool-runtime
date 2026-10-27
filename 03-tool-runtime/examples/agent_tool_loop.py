import asyncio

from asux_tool_runtime.executor.tool_executor import ToolExecutor
from asux_tool_runtime.models.context import PermissionContext
from asux_tool_runtime.registry.tool_registry import InMemoryToolRegistry
from asux_tool_runtime.tools.catalog import register_builtin_tools


async def main():
    # 1. Initialize registry and tools
    registry = InMemoryToolRegistry()
    register_builtin_tools(registry)

    # 2. Define the executor
    executor = ToolExecutor(registry)

    # 3. Create a permission context (e.g., extracted from JWT/Session in production)
    context = PermissionContext(
        principal_id="user_123",
        principal_type="human",
        tenant_id="tenant_001",
        permissions=["product:read", "customer:read"],  # Notice: task:write is missing
    )

    # 4. Simulate LLM suggesting a valid tool call
    print("--- Simulating Valid Tool Call ---")
    result1 = await executor.execute(
        tool_name="product_search", arguments={"query": "coffee"}, context=context
    )
    print(f"Tool: {result1.tool_name} | Success: {result1.success}")
    print(f"Data: {result1.data}")

    # 5. Simulate LLM suggesting an unauthorized tool call
    print("\n--- Simulating Unauthorized Tool Call ---")
    result2 = await executor.execute(
        tool_name="create_task", arguments={"title": "Hack the mainframe"}, context=context
    )
    print(f"Tool: {result2.tool_name} | Success: {result2.success}")
    print(f"Error: {result2.error}")


if __name__ == "__main__":
    asyncio.run(main())
