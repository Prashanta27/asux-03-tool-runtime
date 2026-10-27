import asyncio

import pytest
from pydantic import BaseModel

from asux_tool_runtime.executor.tool_executor import ToolExecutor
from asux_tool_runtime.models.context import PermissionContext
from asux_tool_runtime.models.tool import ToolDefinition
from asux_tool_runtime.registry.tool_registry import InMemoryToolRegistry


class SlowInput(BaseModel):
    sleep_time: float


async def slow_handler(args: SlowInput, context: PermissionContext):
    await asyncio.sleep(args.sleep_time)
    return {"done": True}


class ErrorInput(BaseModel):
    fail: bool


async def error_handler(args: ErrorInput, context: PermissionContext):
    raise RuntimeError("Intentional internal error")


@pytest.fixture
def test_registry() -> InMemoryToolRegistry:
    reg = InMemoryToolRegistry()
    reg.register(
        ToolDefinition(name="slow_tool", description="Slow", input_schema=SlowInput), slow_handler
    )
    reg.register(
        ToolDefinition(name="error_tool", description="Error", input_schema=ErrorInput),
        error_handler,
    )
    return reg


@pytest.mark.asyncio
async def test_executor_success(registry, admin_context):
    executor = ToolExecutor(registry)
    result = await executor.execute("customer_lookup", {"customer_id": "123"}, admin_context)

    assert result.success is True
    assert result.data.customer_id == "123"
    assert result.error is None
    assert result.duration_ms >= 0


@pytest.mark.asyncio
async def test_executor_validation_error(registry, admin_context):
    executor = ToolExecutor(registry)
    # Missing required argument customer_id
    result = await executor.execute("customer_lookup", {}, admin_context)

    assert result.success is False
    assert "Invalid arguments" in result.error


@pytest.mark.asyncio
async def test_executor_authorization_error(registry, read_only_context):
    executor = ToolExecutor(registry)
    # read_only_context lacks 'customer:read'
    result = await executor.execute("customer_lookup", {"customer_id": "123"}, read_only_context)

    assert result.success is False
    assert "lacks required permission" in result.error


@pytest.mark.asyncio
async def test_executor_disabled_tool(registry, admin_context):
    registry.disable_tool("customer_lookup")
    executor = ToolExecutor(registry)

    result = await executor.execute("customer_lookup", {"customer_id": "123"}, admin_context)
    assert result.success is False
    assert "currently disabled" in result.error


@pytest.mark.asyncio
async def test_executor_timeout(test_registry, admin_context):
    executor = ToolExecutor(test_registry, default_timeout=0.1)

    result = await executor.execute("slow_tool", {"sleep_time": 0.5}, admin_context)
    assert result.success is False
    assert "exceeded timeout" in result.error


@pytest.mark.asyncio
async def test_executor_internal_error(test_registry, admin_context):
    executor = ToolExecutor(test_registry)

    result = await executor.execute("error_tool", {"fail": True}, admin_context)
    assert result.success is False
    assert "encountered an internal error" in result.error
