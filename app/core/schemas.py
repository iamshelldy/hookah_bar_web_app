from fastapi import Query
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    id: int
    name: str


class BaseQueryParams(BaseModel):
    id: list[int] | None = Field(Query(None))
    name: list[str] | None = Field(Query(None))

    def model_dump(self, **kwargs) -> dict:
        # Filter None values.
        filtered_data = {
            key: value for key, value in self.__dict__.items() if value is not None
        }
        return filtered_data
