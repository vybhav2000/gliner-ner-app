from pydantic import UUID4
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, APIRouter
from app.models.models import Item, ItemRead
from app.database import get_db
from app.logger import logger

items_router = APIRouter()


@items_router.get("/", response_model=list[ItemRead])
async def read_items(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Item).options(joinedload(Item.entities)).offset(skip).limit(limit)
        )
        items = result.unique().scalars().all()
        return items
    except Exception as e:
        logger.error(f"Error fetching items: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")


@items_router.get("/{item_id}", response_model=ItemRead)
async def read_item(item_id: UUID4, db: AsyncSession = Depends(get_db)):
    logger.info(f"Received request to fetch item with ID: {item_id}")
    result = await db.execute(
        select(Item).where(Item.id == item_id).options(joinedload(Item.entities))
    )
    item = result.unique().scalars().first()
    if not item:
        logger.warning(f"Item with ID {item_id} not found.")
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info(f"Found item with ID {item_id}: {item}")
    return item
