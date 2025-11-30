from fastapi import APIRouter
import logging
from Schemas import HealthCheck
from models import classifier
from helpers.Settings import get_settings

logger=logging.getLogger(__name__)
health=APIRouter(prefix="/api",tags=["health_check"])

@health.get("/health",response_model=HealthCheck)
async def health_check():
    
    return HealthCheck(
        status="healthy",
        model_loaded=classifier.model is not None ,
        total_classes=len(classifier.class_names),
        class_names=classifier.class_names,
        version=get_settings.APP_VERSION
    )
    

