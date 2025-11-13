from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from cheese import models, schemas


async def get_all_cheese_types(db: AsyncSession) -> list[models.DBCheeseType]:
    cheese_types = await db.scalars(select(models.DBCheeseType))

    return cheese_types.all()


async def get_cheese_type_by_id(
    db: AsyncSession,
    cheese_type_id: int
) -> models.DBCheeseType | None:
    return await db.scalar(
        select(models.DBCheeseType).where(models.DBCheeseType.id == cheese_type_id)
    )


async def create_cheese_type(
    db: AsyncSession,
    cheese_type: schemas.CheeseTypeCreate
) -> models.DBCheeseType:
    db_cheese_type = models.DBCheeseType(
        name=cheese_type.name,
        description=cheese_type.description,
    )
    db.add(db_cheese_type)
    await db.commit()
    await db.refresh(db_cheese_type)

    return db_cheese_type


async def get_cheese_type_by_name(
    db: AsyncSession,
    name: str
) -> models.DBCheeseType | None:
    return await db.scalar(
        select(
            models.DBCheeseType
        ).where(
            models.DBCheeseType.name == name
        )
    )


async def get_cheese_list(
    db: AsyncSession,
    packaging_type: models.PackagingType | None = None,
    cheese_type: str | None = None,
) -> list[models.DBCheese]:
    stmt = select(models.DBCheese).options(selectinload(models.DBCheese.cheese_type))

    if packaging_type:
        stmt = stmt.where(models.DBCheese.packaging_type == packaging_type)

    if cheese_type:
        stmt = stmt.join(models.DBCheeseType).where(models.DBCheeseType.name == cheese_type)

    cheese = await db.scalars(stmt)

    return cheese.all()


async def get_cheese_by_id(
    db: AsyncSession,
    cheese_id: int
) -> models.DBCheese | None:
    stmt = select(
        models.DBCheese
    ).where(
        models.DBCheese.id == cheese_id
    ).options(
        joinedload(models.DBCheese.cheese_type)
    )

    return await db.scalar(stmt)


async def get_cheese_by_title(
    db: AsyncSession,
    title: str
) -> models.DBCheese | None:
    stmt = select(
        models.DBCheese
    ).where(
        models.DBCheese.title == title
    ).options(
        joinedload(models.DBCheese.cheese_type)
    )

    return await db.scalar(stmt)


async def create_cheese(
    db: AsyncSession,
    cheese: schemas.CheeseCreate
) -> models.DBCheese:
    db_cheese = models.DBCheese(
        cheese_type_id=cheese.cheese_type_id,
        title=cheese.title,
        price=cheese.price,
        packaging_type=cheese.packaging_type,
    )
    db.add(db_cheese)
    await db.commit()
    await db.refresh(db_cheese, ["cheese_type"])

    return db_cheese
