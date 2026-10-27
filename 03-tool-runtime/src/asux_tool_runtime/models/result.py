from typing import Any

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """
    Consistent, structured output from a tool execution.
    """

    invocation_id: str | None = Field(
        default=None, description="Request/Invocation ID tracking this execution."
    )
    tool_name: str = Field(..., description="Name of the executed tool.")

    success: bool = Field(..., description="Whether execution completed successfully.")

    data: Any | None = Field(default=None, description="The returned data if successful.")
    error: str | None = Field(default=None, description="Safe error message if execution failed.")

    duration_ms: float = Field(default=0.0, description="Execution duration in milliseconds.")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional execution context."
    )
