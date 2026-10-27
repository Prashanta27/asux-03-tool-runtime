
import pytest

from asux_tool_runtime.executor.tool_executor import ToolExecutor


@pytest.mark.asyncio
async def test_customer_lookup(registry, admin_context):
    executor = ToolExecutor(registry)
    result = await executor.execute("customer_lookup", {"customer_id": "cust_001"}, admin_context)

    assert result.success is True
    assert result.data.customer_id == "cust_001"
    assert result.data.name == "Alice Mock"


@pytest.mark.asyncio
async def test_product_search(registry, admin_context):
    executor = ToolExecutor(registry)
    result = await executor.execute("product_search", {"query": "laptop"}, admin_context)

    assert result.success is True
    assert len(result.data.products) == 1
    assert "laptop" in result.data.products[0]["name"]


@pytest.mark.asyncio
async def test_create_task(registry, admin_context):
    executor = ToolExecutor(registry)
    result = await executor.execute(
        "create_task", {"title": "Fix bug", "description": "Fix the UI bug."}, admin_context
    )

    assert result.success is True
    assert result.data.task_id == "task-12345"


@pytest.mark.asyncio
async def test_send_message_requires_permission(registry, read_only_context):
    executor = ToolExecutor(registry)

    result = await executor.execute(
        "send_message", {"recipient_id": "123", "message_body": "Hello"}, read_only_context
    )

    assert result.success is False
    assert "lacks required permission" in result.error
