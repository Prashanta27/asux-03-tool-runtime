import pytest
from pydantic import BaseModel

from asux_tool_runtime.exceptions.errors import ToolNotFoundError, ToolRegistrationError
from asux_tool_runtime.models.tool import ToolDefinition
from asux_tool_runtime.registry.tool_registry import InMemoryToolRegistry


class DummyInput(BaseModel):
    x: int


async def dummy_handler(args: DummyInput, context: dict):
    return {"result": args.x}


@pytest.fixture
def empty_registry() -> InMemoryToolRegistry:
    return InMemoryToolRegistry()


@pytest.fixture
def dummy_tool() -> ToolDefinition:
    return ToolDefinition(name="dummy", description="A dummy tool", input_schema=DummyInput)


def test_register_and_get(empty_registry, dummy_tool):
    empty_registry.register(dummy_tool, dummy_handler)

    definition = empty_registry.get_definition("dummy")
    assert definition.name == "dummy"

    handler = empty_registry.get_handler("dummy")
    assert handler is dummy_handler


def test_duplicate_registration(empty_registry, dummy_tool):
    empty_registry.register(dummy_tool, dummy_handler)
    with pytest.raises(ToolRegistrationError):
        empty_registry.register(dummy_tool, dummy_handler)


def test_get_not_found(empty_registry):
    with pytest.raises(ToolNotFoundError):
        empty_registry.get_definition("unknown")


def test_enable_disable(empty_registry, dummy_tool):
    empty_registry.register(dummy_tool, dummy_handler)

    empty_registry.disable_tool("dummy")
    assert not empty_registry.get_definition("dummy").enabled

    empty_registry.enable_tool("dummy")
    assert empty_registry.get_definition("dummy").enabled
