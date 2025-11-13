from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud
from .enums import PackagingType

router = APIRouter()


@router.get("/cheese_types/", response_model=list[schemas.CheeseType])
async def read_cheese_types(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cheese_types(db=db)


@router.post("/cheese_types/", response_model=schemas.CheeseType)
async def create_cheese_type(
    cheese_type: schemas.CheeseTypeCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_cheese_type = await crud.get_cheese_type_by_name(db=db, name=cheese_type.name)
    if db_cheese_type:
        raise HTTPException(
            status_code=400, detail="Cheese type with this name already exists"
        )

    return await crud.create_cheese_type(
        db=db,
        cheese_type=cheese_type
    )


@router.get("/cheese/", response_model=list[schemas.Cheese])
async def read_cheese(
    db: Annotated[AsyncSession, Depends(get_db)],
    packaging_type: PackagingType | None = None,
    cheese_type: str | None = None,
):
    return await crud.get_cheese_list(
        db=db, packaging_type=packaging_type, cheese_type=cheese_type
    )


@router.get("/cheese/{cheese_id}/", response_model=schemas.Cheese)
async def read_single_cheese(
    cheese_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_cheese = await crud.get_cheese_by_id(db=db, cheese_id=cheese_id)

    if not db_cheese:
        raise HTTPException(status_code=404, detail="Cheese not found")

    return db_cheese


@router.post("/cheese/", response_model=schemas.Cheese)
async def create_cheese(
    cheese: schemas.CheeseCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_cheese = await crud.get_cheese_by_title(db=db, title=cheese.title)
    if db_cheese:
        raise HTTPException(status_code=400, detail="Cheese with this title already exists")

    cheese_type = await crud.get_cheese_type_by_id(db=db, cheese_type_id=cheese.cheese_type_id)
    if not cheese_type:
        raise HTTPException(status_code=400, detail="Cheese type not found")

    return await crud.create_cheese(db=db, cheese=cheese)
