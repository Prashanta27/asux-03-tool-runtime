from pydantic import BaseModel, Field


class PermissionContext(BaseModel):
    """
    Context representing the identity and permissions of the caller.
    """

    principal_id: str = Field(..., description="ID of the calling user or service.")
    principal_type: str = Field(
        ..., description="Type of principal (e.g., 'user', 'service_account')."
    )
    tenant_id: str = Field(..., description="Tenant ID to enforce isolation.")

    permissions: list[str] = Field(
        default_factory=list, description="List of capabilities granted to the caller."
    )
    request_id: str | None = Field(default=None, description="Correlation ID for tracing.")

    extra: dict[str, str] = Field(
        default_factory=dict, description="Additional trusted execution context."
    )
