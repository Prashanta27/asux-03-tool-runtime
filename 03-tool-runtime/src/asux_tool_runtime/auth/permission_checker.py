from typing import Protocol

from asux_tool_runtime.exceptions.errors import ToolAuthorizationError
from asux_tool_runtime.models.context import PermissionContext
from asux_tool_runtime.models.tool import ToolDefinition


class PermissionChecker(Protocol):
    """
    Protocol for checking if a caller is authorized to execute a tool.
    """

    def check_authorization(self, tool: ToolDefinition, context: PermissionContext) -> None:
        """
        Validates the context against the tool's required permissions.
        Raises ToolAuthorizationError if unauthorized.
        """
        ...


class SimplePermissionChecker:
    """
    An in-process permission checker comparing required capabilities against the context.
    """

    def check_authorization(self, tool: ToolDefinition, context: PermissionContext) -> None:
        if not tool.required_permissions:
            return  # Tool requires no specific permissions

        context_permissions = set(context.permissions)

        for required_perm in tool.required_permissions:
            if required_perm not in context_permissions:
                # Security boundary: do not log the full principal context to avoid leaking secrets
                raise ToolAuthorizationError(
                    f"Principal '{context.principal_id}' lacks required permission '{required_perm}' "
                    f"to execute tool '{tool.name}'."
                )
