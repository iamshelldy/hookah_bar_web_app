from fastapi import Query
from pydantic import Field

from app.core.schemas import BaseResponse, BaseQueryParams


class BrandResponse(BaseResponse):
    pass


class CategoryResponse(BaseResponse):
    parent_id: int | None


class FlavourResponse(BaseResponse):
    category_id: int


class TobaccoResponse(BaseResponse):
    strength: int
    brand_id: int


class TobaccoQueryParams(BaseQueryParams):
    strength: list[int] | None = Field(Query(None))
    brand_id: list[int] | None = Field(Query(None))
    flavour_id: list[int] | None = Field(Query(None))
    category_id: list[int] | None = Field(Query(None))
