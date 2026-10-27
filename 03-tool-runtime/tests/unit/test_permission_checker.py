import pytest
from pydantic import BaseModel

from asux_tool_runtime.auth.permission_checker import SimplePermissionChecker
from asux_tool_runtime.exceptions.errors import ToolAuthorizationError
from asux_tool_runtime.models.context import PermissionContext
from asux_tool_runtime.models.tool import ToolDefinition


class DummySchema(BaseModel):
    pass


@pytest.fixture
def checker():
    return SimplePermissionChecker()


def test_permission_checker_success(checker):
    tool = ToolDefinition(
        name="test",
        description="test",
        input_schema=DummySchema,
        required_permissions=["read:all", "write:all"],
    )
    context = PermissionContext(
        principal_id="123",
        principal_type="user",
        tenant_id="t1",
        permissions=["read:all", "write:all", "delete:all"],
    )

    # Should not raise
    checker.check_authorization(tool, context)


def test_permission_checker_missing_perm(checker):
    tool = ToolDefinition(
        name="test",
        description="test",
        input_schema=DummySchema,
        required_permissions=["read:all", "write:all"],
    )
    context = PermissionContext(
        principal_id="123", principal_type="user", tenant_id="t1", permissions=["read:all"]
    )

    with pytest.raises(ToolAuthorizationError, match="lacks required permission 'write:all'"):
        checker.check_authorization(tool, context)


def test_permission_checker_no_required_perms(checker):
    tool = ToolDefinition(
        name="test", description="test", input_schema=DummySchema, required_permissions=[]
    )
    context = PermissionContext(
        principal_id="123", principal_type="user", tenant_id="t1", permissions=[]
    )

    # Should not raise
    checker.check_authorization(tool, context)
