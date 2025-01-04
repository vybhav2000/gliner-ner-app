from fastapi import APIRouter
from app.routers.inference import inference_router
from app.routers.items import items_router


main_router = APIRouter()
main_router.include_router(items_router, prefix="/items", tags=["Items"])
main_router.include_router(inference_router, prefix="/gliner", tags=["Gliner"])
