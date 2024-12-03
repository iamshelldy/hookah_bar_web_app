from sqlalchemy.orm import joinedload

from app.core.dao import BaseDAO
from app.core.database import Session
from app.tobaccos.models import Brand, Category, Flavour, Tobacco, Mapping

from sqlalchemy import select


class BrandDAO(BaseDAO):
    model = Brand


class CategoryDAO(BaseDAO):
    model = Category


class FlavourDAO(BaseDAO):
    model = Flavour


class MappingDAO(BaseDAO):
    model = Mapping


class TobaccoDAO(BaseDAO):
    model = Tobacco

    @classmethod
    async def get_strength_list(cls):
        async with Session() as session:
            query = select(cls.model.strength).group_by(cls.model.strength)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_tobacco(cls, **filters):
        # Обработка category_id
        categories_ids = filters.pop("category_id", None)
        ids_by_category = []
        if categories_ids:
            child_categories_ids = await CategoryDAO.find_all(unique_field="id", parent_id=categories_ids)
            all_categories_ids = categories_ids + child_categories_ids
            flavour_ids_by_category = await FlavourDAO.find_all(unique_field="id", category_id=all_categories_ids)
            ids_by_category = await MappingDAO.find_all(unique_field="tobacco_id", flavour_id=flavour_ids_by_category)

        # Обработка flavour_id
        flavours_ids = filters.pop("flavour_id", None)
        ids_by_flavour = []
        if flavours_ids:
            ids_by_flavour = await MappingDAO.find_all(unique_field="tobacco_id", flavour_id=flavours_ids)

        # Сужение результатов
        if ids_by_category or ids_by_flavour:
            if ids_by_category and ids_by_flavour:
                combined_ids = set(ids_by_category) & set(ids_by_flavour)
            else:
                combined_ids = set(ids_by_category or ids_by_flavour)

            if "id" in filters:
                filters["id"] = list(set(filters["id"]) & combined_ids)
            else:
                filters["id"] = list(combined_ids)

        return await cls.find_all(**filters)

    @classmethod
    async def find_full_data(cls, tobacco_id: int):
        async with Session() as session:
            query = (
                select(Tobacco)
                .options(
                    joinedload(Tobacco.brand),
                    joinedload(Tobacco.mappings).joinedload(Mapping.flavour).joinedload(Flavour.category),
                )
                .filter_by(id=tobacco_id)
            )
            tobacco = (await session.execute(query)).scalar()

            if not tobacco:
                return None

            data = {
                "id": tobacco.id,
                "brand": tobacco.brand.name,
                "name": tobacco.name,
                "categories": set(),
                "flavours": set(),
                "strength": tobacco.strength,
            }

            for mapping in tobacco.mappings:
                if mapping.flavour:
                    data["flavours"].add(mapping.flavour.name)
                    if mapping.flavour.category:
                        data["categories"].add(mapping.flavour.category.name)

            data["flavours"] = list(data["flavours"])
            data["categories"] = list(data["categories"])

            return data

