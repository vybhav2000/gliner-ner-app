from fastapi import FastAPI
from app.database import init_db
from app.routers.routers import main_router
from app.models.gliner_model import GlinerModel


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(main_router)
