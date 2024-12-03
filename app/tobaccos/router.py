from fastapi import APIRouter, HTTPException, Depends

from app.tobaccos.dao import CategoryDAO, FlavourDAO, BrandDAO, TobaccoDAO
from app.tobaccos.schemas import BrandResponse, CategoryResponse, FlavourResponse, TobaccoResponse, TobaccoQueryParams

router = APIRouter(prefix="/api", tags=["router"])


@router.get("/tobacco")
async def get_all_tobacco(query_params: TobaccoQueryParams = Depends()) -> list[TobaccoResponse]:
    return await TobaccoDAO.find_tobacco(**query_params.model_dump())


@router.get("/tobacco/{tobacco_id}")
async def get_tobacco_by_id(tobacco_id: int) -> dict:
    result = await TobaccoDAO.find_full_data(tobacco_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tobacco not found")
    return result


@router.get("/brands")
async def get_all_brands() -> list[BrandResponse]:
    return await BrandDAO.find_all()


@router.get("/brands/{brand_id}")
async def get_brand_by_id(brand_id: int) -> BrandResponse:
    result = await BrandDAO.find_one_or_none_by_id(brand_id)
    if not result:
        raise HTTPException(status_code=404, detail="Brand not found")
    return result


@router.get("/categories")
async def get_all_categories() -> list[CategoryResponse]:
    result = await CategoryDAO.find_all()
    result.sort(key=lambda x: x.parent_id if x.parent_id else x.id)
    return result


@router.get("/categories/{category_id}")
async def get_category_by_id(category_id: int) -> CategoryResponse:
    result = await CategoryDAO.find_one_or_none_by_id(category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return result


@router.get("/flavours")
async def get_all_flavours() -> list[FlavourResponse]:
    return await FlavourDAO.find_all()


@router.get("/flavours/{flavour_id}")
async def get_flavour_by_id(flavour_id: int) -> FlavourResponse:
    result = await FlavourDAO.find_one_or_none_by_id(flavour_id)
    if not result:
        raise HTTPException(status_code=404, detail="Flavour not found")
    return result
