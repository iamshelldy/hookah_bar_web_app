from sqlalchemy.future import select

from app.core.database import Session

class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, unique_field: str | None = None, **filters):
        async with Session() as session:

            # If we need unique field, using GROUP BY.
            if unique_field:
                column = getattr(cls.model, unique_field)
                query = select(column).group_by(column)
            else:
                query = select(cls.model)

            # Apply filters.
            for field, value in filters.items():
                column = getattr(cls.model, field)
                if isinstance(value, list):
                    query = query.filter(column.in_(value))
                else:
                    query = query.filter(column == value)

            result = await session.execute(query)

            return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with Session() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
