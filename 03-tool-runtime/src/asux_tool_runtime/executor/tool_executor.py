import asyncio
import time
from typing import Any

from pydantic import ValidationError

from asux_tool_runtime.auth.permission_checker import PermissionChecker, SimplePermissionChecker
from asux_tool_runtime.exceptions.errors import (
    ToolAuthorizationError,
    ToolDisabledError,
    ToolExecutionError,
    ToolNotFoundError,
    ToolOutputValidationError,
    ToolTimeoutError,
    ToolValidationError,
)
from asux_tool_runtime.models.context import PermissionContext
from asux_tool_runtime.models.result import ToolResult
from asux_tool_runtime.observability.logger import get_logger
from asux_tool_runtime.registry.tool_registry import InMemoryToolRegistry

logger = get_logger(__name__)


class ToolExecutor:
    """
    Standard execution entry point for registered tools.
    Validates arguments, enforces permissions, enforces timeouts, and normalizes output.
    """

    def __init__(
        self,
        registry: InMemoryToolRegistry,
        permission_checker: PermissionChecker | None = None,
        default_timeout: float = 30.0,
    ):
        self.registry = registry
        self.permission_checker = permission_checker or SimplePermissionChecker()
        self.default_timeout = default_timeout

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        context: PermissionContext,
        invocation_id: str | None = None,
    ) -> ToolResult:
        """
        Executes a tool by name with safety checks.
        """
        start_time = time.monotonic()

        try:
            # 1. Resolve Tool
            tool_def = self.registry.get_definition(tool_name)
            handler = self.registry.get_handler(tool_name)

            # 2. Check if Enabled
            if not tool_def.enabled:
                raise ToolDisabledError(f"Tool '{tool_name}' is currently disabled.")

            # 3. Check Authorization
            self.permission_checker.check_authorization(tool_def, context)

            # 4. Validate Input
            try:
                validated_args = tool_def.input_schema.model_validate(arguments)
            except ValidationError as e:
                raise ToolValidationError(f"Invalid arguments for tool '{tool_name}': {e}") from e

            # 5. Execute Handler (with timeout)
            try:
                # We enforce an execution timeout here.
                # Handlers are expected to be async.
                result_data = await asyncio.wait_for(
                    handler(validated_args, context), timeout=self.default_timeout
                )
            except TimeoutError as e:
                # If a timeout occurs after side effects start, report uncertainty accurately.
                raise ToolTimeoutError(
                    f"Tool '{tool_name}' exceeded timeout of {self.default_timeout}s. "
                    "Warning: If this was a side-effecting action, it may have partially or fully completed."
                ) from e
            except Exception as e:
                # Wrap handler exceptions to avoid leaking internal stack traces up the stack
                logger.error(f"Tool execution failed for '{tool_name}': {e}", exc_info=True)
                raise ToolExecutionError(
                    f"Tool '{tool_name}' encountered an internal error during execution."
                ) from e

            # 6. Validate Output (if schema is provided)
            if tool_def.output_schema:
                try:
                    result_data = tool_def.output_schema.model_validate(result_data)
                except ValidationError as e:
                    raise ToolOutputValidationError(
                        f"Tool '{tool_name}' returned invalid output format: {e}"
                    ) from e

            duration_ms = (time.monotonic() - start_time) * 1000

            # 7. Return Structured Result
            return ToolResult(
                invocation_id=invocation_id or context.request_id,
                tool_name=tool_name,
                success=True,
                data=result_data,
                duration_ms=duration_ms,
            )

        except (
            ToolNotFoundError,
            ToolDisabledError,
            ToolValidationError,
            ToolAuthorizationError,
            ToolExecutionError,
            ToolTimeoutError,
            ToolOutputValidationError,
        ) as e:
            # Expected runtime errors - return as a failed ToolResult rather than throwing raw exceptions
            # so the caller (Agent/LLM) can see the structured failure and recover.
            duration_ms = (time.monotonic() - start_time) * 1000
            logger.warning(f"Tool execution rejected/failed: {e!s}")
            return ToolResult(
                invocation_id=invocation_id or context.request_id,
                tool_name=tool_name,
                success=False,
                error=str(e),
                duration_ms=duration_ms,
            )
        except Exception as e:
            # Absolute fallback for unexpected framework bugs
            duration_ms = (time.monotonic() - start_time) * 1000
            logger.error(f"Critical framework error during tool execution: {e!s}", exc_info=True)
            return ToolResult(
                invocation_id=invocation_id or context.request_id,
                tool_name=tool_name,
                success=False,
                error="An unexpected system error occurred while executing the tool.",
                duration_ms=duration_ms,
            )
