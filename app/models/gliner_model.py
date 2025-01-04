import os
import torch.cuda
from gliner import GLiNER
from app.schema import Entity
from app.logger import logger

MODEL_NAME = os.getenv("MODEL_NAME")

class GlinerModel:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading the model into the device: {self.device}")
        self.model = GLiNER.from_pretrained(MODEL_NAME)
        self.model.to(torch.device(self.device))
        logger.info("GLinerModel object created and ready.")

    def predict_entities(self, text, labels, threshold=0.3):
        entities = self.model.predict_entities(text, labels, threshold=threshold)
        predictions = []
        for entity in entities:
            entity_object = Entity(entity=entity["text"], label=entity["label"])
            predictions.append(entity_object)
        return predictions

gliner_object = GlinerModel()
