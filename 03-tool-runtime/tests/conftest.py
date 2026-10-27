import pytest

from asux_tool_runtime.models.context import PermissionContext
from asux_tool_runtime.registry.tool_registry import InMemoryToolRegistry
from asux_tool_runtime.tools.catalog import register_builtin_tools


@pytest.fixture
def registry() -> InMemoryToolRegistry:
    reg = InMemoryToolRegistry()
    register_builtin_tools(reg)
    return reg


@pytest.fixture
def admin_context() -> PermissionContext:
    return PermissionContext(
        principal_id="admin-1",
        principal_type="user",
        tenant_id="tenant-1",
        permissions=[
            "customer:read",
            "product:read",
            "order:read",
            "conversation:read",
            "task:write",
            "message:write",
        ],
    )


@pytest.fixture
def read_only_context() -> PermissionContext:
    return PermissionContext(
        principal_id="viewer-1",
        principal_type="user",
        tenant_id="tenant-1",
        permissions=["product:read"],
    )
