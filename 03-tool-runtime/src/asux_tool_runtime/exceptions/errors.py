class ToolRuntimeError(Exception):
    """Base exception for all Tool Runtime errors."""

    pass


class ToolNotFoundError(ToolRuntimeError):
    """Raised when a tool name is not found in the registry."""

    pass


class ToolRegistrationError(ToolRuntimeError):
    """Raised when trying to register a tool that already exists or is invalid."""

    pass


class ToolValidationError(ToolRuntimeError):
    """Raised when tool arguments fail schema validation."""

    pass


class ToolAuthorizationError(ToolRuntimeError):
    """Raised when the caller lacks required permissions."""

    pass


class ToolDisabledError(ToolRuntimeError):
    """Raised when attempting to execute a disabled tool."""

    pass


class ToolExecutionError(ToolRuntimeError):
    """Raised when the tool handler raises an exception during execution."""

    pass


class ToolTimeoutError(ToolRuntimeError):
    """Raised when tool execution exceeds the permitted timeout."""

    pass


class ToolOutputValidationError(ToolRuntimeError):
    """Raised when the tool's output fails schema validation."""

    pass


class ToolPolicyError(ToolRuntimeError):
    """Raised when a policy blocks execution."""

    pass


class ToolRegistryError(ToolRuntimeError):
    """Raised when the tool registry fails to read or write data."""

    pass
