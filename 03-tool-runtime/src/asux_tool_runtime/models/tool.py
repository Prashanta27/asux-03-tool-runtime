from typing import Any

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    """
    Defines a tool's metadata, schemas, and permissions.
    """

    name: str = Field(..., description="Stable, unique tool identifier.")
    description: str = Field(..., description="What the tool does and when it should be used.")

    input_schema: type[BaseModel] = Field(
        ..., description="Pydantic model representing expected arguments."
    )
    output_schema: type[BaseModel] | None = Field(
        default=None, description="Optional expected output schema."
    )

    version: str = Field(default="1.0.0", description="Tool version.")
    category: str | None = Field(
        default=None, description="Optional category (e.g., 'customer', 'product')."
    )

    required_permissions: list[str] = Field(
        default_factory=list, description="Required capabilities to execute."
    )
    risk_level: str = Field(
        default="low", description="Appropriate risk classification (low, medium, high)."
    )

    enabled: bool = Field(default=True, description="Whether the tool is available for execution.")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional structured metadata."
    )

    # Using Callable[[Any, Any], Awaitable[Any]] where args are (validated_input, permission_context)
    # Excluded from Pydantic validation because it's not easily serializable. We can just store it in the registry directly alongside the definition, or exclude it here.
    # Let's keep it clean: ToolDefinition is just the data. The Registry binds it to a handler.
