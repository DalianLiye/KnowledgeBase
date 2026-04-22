[目录](../目录.md)



# 关于工具调用策略
对于不支持原生结构化输出的模型，LangChain 使用工具调用来实现相同的效果。这适用于所有支持工具调用的模型（大多数现代模型都支持）。
要使用此策略，请配置 ToolStrategy：
```python
class ToolStrategy(Generic[SchemaT]):
    schema: type[SchemaT]
    tool_message_content: str | None
    handle_errors: Union[
        bool,
        str,
        type[Exception],
        tuple[type[Exception], ...],
        Callable[[Exception], str],
    ]
```
schema (必填参数)
用于定义结构化输出格式的 Schema，支持以下几种类型：
- Pydantic 模型：继承自 BaseModel 的子类，自带字段校验，返回经过验证的 Pydantic 实例。
- 数据类 (Dataclasses)：带类型注解的 Python 数据类，返回字典。
- TypedDict：类型化字典类，返回字典。
- JSON Schema：符合 JSON Schema 规范的字典，返回字典。
- Union 类型：多个 Schema 选项，模型会根据上下文选择最合适的 Schema

tool_message_content
当生成结构化输出时，返回的工具消息的自定义内容。如果未提供，默认显示结构化响应数据。

handle_errors
结构化输出验证失败时的错误处理策略。默认值为 True。
- True：使用默认错误模板捕获所有错误
- str：使用此自定义消息捕获所有错误
- type[Exception]：仅使用默认消息捕获此异常类型
- tuple[type[Exception], ...]：仅使用默认消息捕获这些异常类型
- Callable[[Exception], str]：返回错误消息的自定义函数
- False：不重试，让异常向上抛出

Pydantic Model
```python
from pydantic import BaseModel, Field
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ProductReview(BaseModel):
    """Analysis of a product review."""
    rating: int | None = Field(description="The rating of the product", ge=1, le=5)
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review")
    key_points: list[str] = Field(description="The key points of the review. Lowercase, 1-3 words each.")

agent = create_agent(
    model="gpt-5",
    tools=tools,
    response_format=ToolStrategy(ProductReview)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# ProductReview(rating=5, sentiment='positive', key_points=['fast shipping', 'expensive'])
```

Dataclass
```python
from dataclasses import dataclass
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


@dataclass
class ProductReview:
    """Analysis of a product review."""
    rating: int | None  # The rating of the product (1-5)
    sentiment: Literal["positive", "negative"]  # The sentiment of the review
    key_points: list[str]  # The key points of the review

agent = create_agent(
    model="gpt-5",
    tools=tools,
    response_format=ToolStrategy(ProductReview)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# {'rating': 5, 'sentiment': 'positive', 'key_points': ['fast shipping', 'expensive']}
```

TypedDict
```python
from typing import Literal
from typing_extensions import TypedDict
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ProductReview(TypedDict):
    """Analysis of a product review."""
    rating: int | None  # The rating of the product (1-5)
    sentiment: Literal["positive", "negative"]  # The sentiment of the review
    key_points: list[str]  # The key points of the review

agent = create_agent(
    model="gpt-5",
    tools=tools,
    response_format=ToolStrategy(ProductReview)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# {'rating': 5, 'sentiment': 'positive', 'key_points': ['fast shipping', 'expensive']}
```


JSON Schema
```python
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


product_review_schema = {
    "type": "object",
    "description": "Analysis of a product review.",
    "properties": {
        "rating": {
            "type": ["integer", "null"],
            "description": "The rating of the product (1-5)",
            "minimum": 1,
            "maximum": 5
        },
        "sentiment": {
            "type": "string",
            "enum": ["positive", "negative"],
            "description": "The sentiment of the review"
        },
        "key_points": {
            "type": "array",
            "items": {"type": "string"},
            "description": "The key points of the review"
        }
    },
    "required": ["sentiment", "key_points"]
}

agent = create_agent(
    model="gpt-5",
    tools=tools,
    response_format=ToolStrategy(product_review_schema)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# {'rating': 5, 'sentiment': 'positive', 'key_points': ['fast shipping', 'expensive']}
```

Union Types
```python
from pydantic import BaseModel, Field
from typing import Literal, Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ProductReview(BaseModel):
    """Analysis of a product review."""
    rating: int | None = Field(description="The rating of the product", ge=1, le=5)
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review")
    key_points: list[str] = Field(description="The key points of the review. Lowercase, 1-3 words each.")

class CustomerComplaint(BaseModel):
    """A customer complaint about a product or service."""
    issue_type: Literal["product", "service", "shipping", "billing"] = Field(description="The type of issue")
    severity: Literal["low", "medium", "high"] = Field(description="The severity of the complaint")
    description: str = Field(description="Brief description of the complaint")

agent = create_agent(
    model="gpt-5",
    tools=tools,
    response_format=ToolStrategy(Union[ProductReview, CustomerComplaint])
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# ProductReview(rating=5, sentiment='positive', key_points=['fast shipping', 'expensive'])
```

# 自定义工具消息内容
tool_message_content 参数允许你自定义，当生成结构化输出时，出现在对话历史中的消息内容

```python
from pydantic import BaseModel, Field
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class MeetingAction(BaseModel):
    """Action items extracted from a meeting transcript."""
    task: str = Field(description="The specific task to be completed")
    assignee: str = Field(description="Person responsible for the task")
    priority: Literal["low", "medium", "high"] = Field(description="Priority level")

agent = create_agent(
    model="gpt-5",
    tools=[],
    response_format=ToolStrategy(
        schema=MeetingAction,
        tool_message_content="Action item captured and added to meeting notes!"
    )
)

agent.invoke({
    "messages": [{"role": "user", "content": "From our meeting: Sarah needs to update the project timeline as soon as possible"}]
})
```

```text
================================ Human Message =================================

From our meeting: Sarah needs to update the project timeline as soon as possible
================================== Ai Message ==================================
Tool Calls:
  MeetingAction (call_1)
 Call ID: call_1
  Args:
    task: Update the project timeline
    assignee: Sarah
    priority: high
================================= Tool Message =================================
Name: MeetingAction

Action item captured and added to meeting notes!
```

Without tool_message_content, our final ToolMessage would be:
```text
================================= Tool Message =================================
Name: MeetingAction

Returning structured response: {'task': 'update the project timeline', 'assignee': 'Sarah', 'priority': 'high'}
```

# 错误处理

模型在通过工具调用生成结构化输出时，可能会出现错误
LangChain 提供了智能重试机制，可以自动处理这些错误

**多结构化输出错误**\
当模型错误地调用了多个结构化输出工具时，智能体会通过 ToolMessage 提供错误反馈，并提示模型重试：
```python
from pydantic import BaseModel, Field
from typing import Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ContactInfo(BaseModel):
    name: str = Field(description="Person's name")
    email: str = Field(description="Email address")

class EventDetails(BaseModel):
    event_name: str = Field(description="Name of the event")
    date: str = Field(description="Event date")

agent = create_agent(
    model="gpt-5",
    tools=[],
    response_format=ToolStrategy(Union[ContactInfo, EventDetails])  # Default: handle_errors=True
)

agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})
```

```text
================================ Human Message =================================

Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th
None
================================== Ai Message ==================================
Tool Calls:
  ContactInfo (call_1)
 Call ID: call_1
  Args:
    name: John Doe
    email: john@email.com
  EventDetails (call_2)
 Call ID: call_2
  Args:
    event_name: Tech Conference
    date: March 15th
================================= Tool Message =================================
Name: ContactInfo

Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected.
 Please fix your mistakes.
================================= Tool Message =================================
Name: EventDetails

Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected.
 Please fix your mistakes.
================================== Ai Message ==================================
Tool Calls:
  ContactInfo (call_3)
 Call ID: call_3
  Args:
    name: John Doe
    email: john@email.com
================================= Tool Message =================================
Name: ContactInfo

Returning structured response: {'name': 'John Doe', 'email': 'john@email.com'}
```

**Schema 校验错误**\
当结构化输出与预期的 Schema 不匹配时，智能体会提供具体的错误反馈：
```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ProductRating(BaseModel):
    rating: int | None = Field(description="Rating from 1-5", ge=1, le=5)
    comment: str = Field(description="Review comment")

agent = create_agent(
    model="gpt-5",
    tools=[],
    response_format=ToolStrategy(ProductRating),  # Default: handle_errors=True
    system_prompt="You are a helpful assistant that parses product reviews. Do not make any field or value up."
)

agent.invoke({
    "messages": [{"role": "user", "content": "Parse this: Amazing product, 10/10!"}]
})
```

```text
================================ Human Message =================================

Parse this: Amazing product, 10/10!
================================== Ai Message ==================================
Tool Calls:
  ProductRating (call_1)
 Call ID: call_1
  Args:
    rating: 10
    comment: Amazing product
================================= Tool Message =================================
Name: ProductRating

Error: Failed to parse structured output for tool 'ProductRating': 1 validation error for ProductRating.rating
  Input should be less than or equal to 5 [type=less_than_equal, input_value=10, input_type=int].
 Please fix your mistakes.
================================== Ai Message ==================================
Tool Calls:
  ProductRating (call_2)
 Call ID: call_2
  Args:
    rating: 5
    comment: Amazing product
================================= Tool Message =================================
Name: ProductRating

Returning structured response: {'rating': 5, 'comment': 'Amazing product'}
```


**错误处理策略**\
你可以通过 handle_errors 参数自定义错误的处理方式：

- Custom error message:
  ```python
  ToolStrategy(
      schema=ProductRating,
      handle_errors="Please provide a valid rating between 1-5 and include a comment."
  )
  ```
  
  如果 handle_errors 是一个字符串，智能体将始终使用固定的工具消息提示模型重试：
  ```text
  ================================= Tool Message =================================
  Name: ProductRating

  Please provide a valid rating between 1-5 and include a comment.
  ```

- Handle specific exceptions only:
  ```python
  ToolStrategy(
      schema=ProductRating,
      handle_errors=ValueError  # Only retry on ValueError, raise others
  )
  ```
  如果 handle_errors 是一个异常元组，那么智能体仅在抛出的异常是指定类型之一时，才会使用默认错误消息进行重试。其他所有情况，异常都会直接抛出


- Handle multiple exception types:
  ```python
  ToolStrategy(
      schema=ProductRating,
      handle_errors=(ValueError, TypeError)  # Retry on ValueError and TypeError
  )
  ```
  如果 handle_errors 是一个异常元组，那么智能体仅在抛出的异常是指定类型之一时，才会使用默认错误消息进行重试。其他所有情况，异常都会直接抛出





- Custom error handler function:
  ```python
  from langchain.agents.structured_output import StructuredOutputValidationError
  from langchain.agents.structured_output import MultipleStructuredOutputsError

  def custom_error_handler(error: Exception) -> str:
      if isinstance(error, StructuredOutputValidationError):
          return "There was an issue with the format. Try again."
      elif isinstance(error, MultipleStructuredOutputsError):
          return "Multiple structured outputs were returned. Pick the most relevant one."
      else:
          return f"Error: {str(error)}"


  agent = create_agent(
      model="gpt-5",
      tools=[],
      response_format=ToolStrategy(
                          schema=Union[ContactInfo, EventDetails],
                          handle_errors=custom_error_handler
                      )  # Default: handle_errors=True
  )

  result = agent.invoke({
      "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
  })

  for msg in result['messages']:
      # If message is actually a ToolMessage object (not a dict), check its class name
      if type(msg).__name__ == "ToolMessage":
          print(msg.content)
      # If message is a dictionary or you want a fallback
      elif isinstance(msg, dict) and msg.get('tool_call_id'):
          print(msg['content'])
  ```

  On StructuredOutputValidationError:
  ```text
  ================================= Tool Message =================================
  Name: ToolStrategy

  There was an issue with the format. Try again.
  ```

  On MultipleStructuredOutputsError:
  ```python
  ================================= Tool Message =================================
  Name: ToolStrategy

  Multiple structured outputs were returned. Pick the most relevant one.
  ```

  On other errors:
  ```python 
  ================================= Tool Message =================================
  Name: ToolStrategy

  Error: <error message>
  ```


- No error handling:
  ```python
  response_format = ToolStrategy(
      schema=ProductRating,
      handle_errors=False  # All errors raised
  )
  ```