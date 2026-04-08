可以请求模型以与给定模式匹配的格式提供其响应\
这对于确保输出可以被轻松解析并用于后续处理非常有用\
LangChain 支持多种模式类型以及强制结构化输出的方法。

- Pydantic\
  Pydantic 模型提供了最丰富的功能集，包括字段验证、描述和嵌套结构

  示例：
  ```python
  from pydantic import BaseModel, Field

  class Movie(BaseModel):
      """A movie with details."""
      title: str = Field(description="The title of the movie")
      year: int = Field(description="The year the movie was released")
      director: str = Field(description="The director of the movie")
      rating: float = Field(description="The movie's rating out of 10")

  model_with_structure = model.with_structured_output(Movie)
  response = model_with_structure.invoke("Provide details about the movie Inception")
  print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)
  ```

- TypedDict\
  Python 的 TypedDict 提供了比 Pydantic 模型更简单的替代方案，非常适合在不需要运行时验证时使用。
  ```python
  from typing_extensions import TypedDict, Annotated

  class MovieDict(TypedDict):
      """A movie with details."""
      title: Annotated[str, ..., "The title of the movie"]
      year: Annotated[int, ..., "The year the movie was released"]
      director: Annotated[str, ..., "The director of the movie"]
      rating: Annotated[float, ..., "The movie's rating out of 10"]

  model_with_structure = model.with_structured_output(MovieDict)
  response = model_with_structure.invoke("Provide details about the movie Inception")
  print(response)  # {'title': 'Inception', 'year': 2010, 'director': 'Christopher Nolan', 'rating': 8.8}
  ```

- JSON Schema\
  提供用于最大控制和互操作性的 JSON 模式
  ```python
  import json

  json_schema = {
      "title": "Movie",
      "description": "A movie with details",
      "type": "object",
      "properties": {
          "title": {
              "type": "string",
              "description": "The title of the movie"
          },
          "year": {
              "type": "integer",
              "description": "The year the movie was released"
          },
          "director": {
              "type": "string",
              "description": "The director of the movie"
          },
          "rating": {
              "type": "number",
              "description": "The movie's rating out of 10"
          }
      },
      "required": ["title", "year", "director", "rating"]
  }

  model_with_structure = model.with_structured_output(
      json_schema,
      method="json_schema",
  )
  response = model_with_structure.invoke("Provide details about the movie Inception")
  print(response)  # {'title': 'Inception', 'year': 2010, ...}
  ```

**注意事项**
- 方法参数（Method parameter）\
  有些模型提供者支持多种生成结构化输出的方式，可以通过方法参数选择使用哪一种\
  可选方法包括：
  - 'json_schema'：使用提供者内建的结构化输出功能，直接按照给定的 JSON Schema 生成结构化内容（优点：通常更可靠，框架会帮助解析与校验）
  - 'function_calling'：通过强制模型发起一个“函数/工具调用”（tool call）的方式来得到结构化输出，模型会把调用参数（通常符合你给的 schema）作为结构化结果返回（常见于 OpenAI 的 function-calling 功能）
  - 'json_mode'：某些提供者在 'json_schema' 之前提供的早期模式，要求模型生成有效的 JSON，但这里的 schema 需要你自己在 prompt（提示）里描述（可靠性和自动校验性通常不如 json_schema）
- 包含原始（Include raw）\
  把 include_raw=True 传给调用可以同时得到解析后的结构化结果和原始的 AIMessage（模型原始返回的消息），保留原始消息有助于访问元数据（比如 token 计数）或在解析失败时回滚查看原始文本
- 校验（Validation）\
  - 使用 Pydantic 模型（或类似工具）的好处是可以自动进行类型和结构校验（自动抛出不符合规则的错误或进行转换）
  - 如果你使用 TypedDict（Python 类型提示的一种形式）或纯 JSON Schema，则通常需要自行实现校验逻辑（手动调用校验器或写校验代码），不会像 Pydantic 那样自动帮你做所有校验和类型转换。


示例：\
在把模型返回的结构化内容解析成你需要的数据结构的同时，保留并返回原始的 AIMessage 对象也很有用，因为原始对象包含一些解析后不可见的响应元数据（例如令牌计数 token counts）\
如果在调用 with_structured_output 时想同时得到解析后的数据和原始的 AIMessage，就把参数 include_raw=True 传进去

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")

model_with_structure = model.with_structured_output(Movie, include_raw=True)
response = model_with_structure.invoke("Provide details about the movie Inception")
response
# {
#     "raw": AIMessage(...),
#     "parsed": Movie(title=..., year=..., ...),
#     "parsing_error": None,
# }
```

示例：schema可以嵌套
```python
from typing_extensions import Annotated, TypedDict

class Actor(TypedDict):
    name: str
    role: str

class MovieDetails(TypedDict):
    title: str
    year: int
    cast: list[Actor]
    genres: list[str]
    budget: Annotated[float | None, ..., "Budget in millions USD"]

model_with_structure = model.with_structured_output(MovieDetails)
```