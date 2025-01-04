from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.logger import logger
from app.schema import InferenceRequest, InferenceResponse
from app.models.models import Item, Entity
from app.database import get_db
from app.models.gliner_model import gliner_object, GlinerModel

inference_router = APIRouter()


def get_gliner_model() -> GlinerModel:
    return gliner_object


@inference_router.post("/predict", response_model=InferenceResponse)
async def predict_entities(
    request: InferenceRequest,
    session: AsyncSession = Depends(get_db),
    gliner_model: GlinerModel = Depends(get_gliner_model),
):
    """
    Endpoint to get entities predicted by GLiNER model for a given text and labels.
    Also writes the query and predicted entities to the database using UUIDs.
    """
    try:
        logger.info(f"Received prediction request for text: {request.text}")

        predictions = gliner_model.predict_entities(request.text, request.labels)
        logger.info(f"Predicted entities: {predictions}")

        new_query = Item(id=uuid4(), query=request.text)
        session.add(new_query)
        await session.commit()
        await session.refresh(new_query)

        for entity in predictions:
            new_entity = Entity(
                entity=entity.entity, label=entity.label, item_id=new_query.id
            )
            session.add(new_entity)
        await session.commit()
        await session.close()
        response = InferenceResponse(query_id=new_query.id, entities=predictions)
        logger.info(f"Response for query {new_query.id}: {response}")
        return response
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error during inference: {str(e)}")
