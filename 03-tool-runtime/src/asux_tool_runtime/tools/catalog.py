from typing import Any

from pydantic import BaseModel, Field

from asux_tool_runtime.models.context import PermissionContext
from asux_tool_runtime.models.tool import ToolDefinition


# ---------------------------------------------------------------------------
# Customer Tool
# ---------------------------------------------------------------------------
class CustomerLookupInput(BaseModel):
    customer_id: str = Field(..., description="ID of the customer to look up.")


class CustomerLookupOutput(BaseModel):
    customer_id: str
    name: str
    email: str


async def customer_lookup_handler(
    args: CustomerLookupInput, context: PermissionContext
) -> CustomerLookupOutput:
    # Mock data adapter
    return CustomerLookupOutput(
        customer_id=args.customer_id, name="Alice Mock", email="alice@mock.com"
    )


CUSTOMER_LOOKUP_TOOL = ToolDefinition(
    name="customer_lookup",
    description="Look up a customer's basic information by ID.",
    input_schema=CustomerLookupInput,
    output_schema=CustomerLookupOutput,
    required_permissions=["customer:read"],
    risk_level="low",
)


# ---------------------------------------------------------------------------
# Product Tool
# ---------------------------------------------------------------------------
class ProductSearchInput(BaseModel):
    query: str = Field(..., description="Search query for products.")


class ProductSearchOutput(BaseModel):
    products: list[dict[str, str | float]]


async def product_search_handler(
    args: ProductSearchInput, context: PermissionContext
) -> ProductSearchOutput:
    return ProductSearchOutput(
        products=[{"id": "p1", "name": f"Mock Product matching '{args.query}'", "price": 99.99}]
    )


PRODUCT_SEARCH_TOOL = ToolDefinition(
    name="product_search",
    description="Search for product information and pricing.",
    input_schema=ProductSearchInput,
    output_schema=ProductSearchOutput,
    required_permissions=["product:read"],
    risk_level="low",
)


# ---------------------------------------------------------------------------
# Order Tool
# ---------------------------------------------------------------------------
class OrderLookupInput(BaseModel):
    order_id: str = Field(..., description="The ID of the order.")


class OrderLookupOutput(BaseModel):
    order_id: str
    status: str
    total_amount: float


async def order_lookup_handler(
    args: OrderLookupInput, context: PermissionContext
) -> OrderLookupOutput:
    return OrderLookupOutput(order_id=args.order_id, status="shipped", total_amount=150.00)


ORDER_LOOKUP_TOOL = ToolDefinition(
    name="order_lookup",
    description="Retrieve the status and details of a customer order.",
    input_schema=OrderLookupInput,
    output_schema=OrderLookupOutput,
    required_permissions=["order:read"],
    risk_level="low",
)


# ---------------------------------------------------------------------------
# Conversation Tool
# ---------------------------------------------------------------------------
class ConversationLookupInput(BaseModel):
    conversation_id: str = Field(..., description="ID of the conversation transcript to fetch.")


class ConversationLookupOutput(BaseModel):
    conversation_id: str
    messages: list[str]


async def conversation_lookup_handler(
    args: ConversationLookupInput, context: PermissionContext
) -> ConversationLookupOutput:
    return ConversationLookupOutput(
        conversation_id=args.conversation_id,
        messages=["Hello", "I need help", "Sure, what is the issue?"],
    )


CONVERSATION_LOOKUP_TOOL = ToolDefinition(
    name="conversation_lookup",
    description="Retrieve a historical conversation.",
    input_schema=ConversationLookupInput,
    output_schema=ConversationLookupOutput,
    required_permissions=["conversation:read"],
    risk_level="low",
)


# ---------------------------------------------------------------------------
# Task Tool (Side effect)
# ---------------------------------------------------------------------------
class CreateTaskInput(BaseModel):
    title: str = Field(..., description="Title of the task.")
    description: str = Field(default="", description="Detailed task description.")


class CreateTaskOutput(BaseModel):
    task_id: str
    status: str


async def create_task_handler(
    args: CreateTaskInput, context: PermissionContext
) -> CreateTaskOutput:
    # MOCK side effect. We don't actually write to a DB.
    return CreateTaskOutput(task_id="task-12345", status="created")


CREATE_TASK_TOOL = ToolDefinition(
    name="create_task",
    description="Create a new task in the project management system.",
    input_schema=CreateTaskInput,
    output_schema=CreateTaskOutput,
    required_permissions=["task:write"],
    risk_level="medium",
)


# ---------------------------------------------------------------------------
# Message Tool (Side effect)
# ---------------------------------------------------------------------------
class SendMessageInput(BaseModel):
    recipient_id: str = Field(..., description="ID of the recipient.")
    message_body: str = Field(..., description="Content of the message to send.")


class SendMessageOutput(BaseModel):
    success: bool
    delivered_at: str


async def send_message_handler(
    args: SendMessageInput, context: PermissionContext
) -> SendMessageOutput:
    # MOCK side effect. We explicitly note this is a mock.
    return SendMessageOutput(success=True, delivered_at="2026-10-10T12:00:00Z")


SEND_MESSAGE_TOOL = ToolDefinition(
    name="send_message",
    description="Simulate sending a message to a recipient. Does NOT actually send an email or SMS.",
    input_schema=SendMessageInput,
    output_schema=SendMessageOutput,
    required_permissions=["message:write"],
    risk_level="high",
)


# ---------------------------------------------------------------------------
# Registry Helper
# ---------------------------------------------------------------------------
def register_builtin_tools(registry: Any) -> None:
    """Registers all built-in catalog tools into a provided ToolRegistry."""
    registry.register(CUSTOMER_LOOKUP_TOOL, customer_lookup_handler)
    registry.register(PRODUCT_SEARCH_TOOL, product_search_handler)
    registry.register(ORDER_LOOKUP_TOOL, order_lookup_handler)
    registry.register(CONVERSATION_LOOKUP_TOOL, conversation_lookup_handler)
    registry.register(CREATE_TASK_TOOL, create_task_handler)
    registry.register(SEND_MESSAGE_TOOL, send_message_handler)
