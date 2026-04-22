from pydantic import BaseModel
from typing import Any, Optional, TypeVar, Generic, List

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None

    class Config:
        from_attributes = True

    @classmethod
    def success(cls, data: Any = None, message: str = "success", code: int = 200):
        return cls(code=code, message=message, data=data)

    @classmethod
    def error(cls, message: str = "error", code: int = 400):
        return cls(code=code, message=message, data=None)


class PageResponse(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    items: List[T]
