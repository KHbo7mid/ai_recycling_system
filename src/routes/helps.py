from fastapi import APIRouter ,HTTPException,status
from fastapi.responses import JSONResponse
from Services import ClassificationService
from typing import List
from Schemas import ClassInfo
import logging 
logger=logging.getLogger(__name__)
helper_router=APIRouter(prefix="/api",tags=["helper_routers"])

@helper_router.get("/recycling-guide")
async def get_recycling_guide():
    class_info=ClassificationService.get_detailed_class_information()
    guide={
        "materials": class_info,
        "general_tips": [
            "Always clean containers before recycling",
            "Remove lids and caps when required",
            "Flatten cardboard boxes to save space",
            "Check local recycling guidelines for specific rules",
            "When in doubt, throw it out to avoid contamination"
        ]
    }
    return JSONResponse(
        content={
            "guide":guide
        }
    )
    
@helper_router.get("/classes",response_model=List[ClassInfo])
async def get_classes():
    try:
        class_info = ClassificationService.get_detailed_class_information()
        return class_info
    except Exception as e:
        logger.error(f"Error getting class info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error retrieving class information"
        )