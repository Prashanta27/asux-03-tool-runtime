from collections.abc import Awaitable, Callable
from typing import Any

from asux_tool_runtime.exceptions.errors import ToolNotFoundError, ToolRegistrationError
from asux_tool_runtime.models.tool import ToolDefinition

# A handler takes (validated_args, permission_context) and returns some Any data (which we will validate).
ToolHandler = Callable[[Any, Any], Awaitable[Any]]


class InMemoryToolRegistry:
    """
    In-memory storage binding ToolDefinitions to executable Handlers.
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}
        self._handlers: dict[str, ToolHandler] = {}

    def register(self, definition: ToolDefinition, handler: ToolHandler) -> None:
        """Registers a tool and its handler."""
        if definition.name in self._tools:
            raise ToolRegistrationError(f"Tool '{definition.name}' is already registered.")

        # In a real system, we'd also validate that the handler has the correct signature
        self._tools[definition.name] = definition
        self._handlers[definition.name] = handler

    def get_definition(self, name: str) -> ToolDefinition:
        """Retrieves a tool definition by name."""
        if name not in self._tools:
            raise ToolNotFoundError(f"Tool '{name}' not found in registry.")
        return self._tools[name]

    def get_handler(self, name: str) -> ToolHandler:
        """Retrieves a tool handler by name."""
        if name not in self._handlers:
            raise ToolNotFoundError(f"Handler for tool '{name}' not found.")
        return self._handlers[name]

    def list_definitions(self, include_disabled: bool = False) -> list[ToolDefinition]:
        """Lists all registered tool definitions."""
        return [tool for tool in self._tools.values() if tool.enabled or include_disabled]

    def enable_tool(self, name: str) -> None:
        """Enables a disabled tool."""
        tool = self.get_definition(name)
        tool.enabled = True

    def disable_tool(self, name: str) -> None:
        """Disables a tool."""
        tool = self.get_definition(name)
        tool.enabled = False
