from fastapi import APIRouter,UploadFile,File,HTTPException,status
from fastapi.responses import StreamingResponse
from Schemas import ClassificationResponse
import logging
from helpers.Settings import get_settings
import numpy as np
import cv2 ,io 
from typing import List
from Schemas import ClassInfo
from Services import ClassificationService
logger=logging.getLogger(__name__)

router_classify=APIRouter(prefix="/api/classify",tags=["Classification"])

@router_classify.post("",response_model=ClassificationResponse)
async def classify_image(file:UploadFile = File(...)):
    if file.content_type not in get_settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed types: {', '.join(get_settings.ALLOWED_IMAGE_TYPES)}"
        )
    try:
        #validate file size(max 10MB)
        max_size=10*1024*1024
        contents=await file.read()
        if len(contents) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Maximum size is 10MB."
            )
        # Decode Image
        nparr=np.frombuffer(contents,np.uint8)
        image=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not decode image. Please check the file format."
            )
        #Convert BGR to RGB
        image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        #perform classification 
        result =ClassificationService.classify_image(image=image_rgb)
        
        logger.info(
            f"Classification completed: {result['total_objects']} objects detected, "
            f"time: {result['processing_time']:.2f}s"
        )
        
        return ClassificationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Classification error : {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error processing image. Please try again."
        )
        
@router_classify.post("/annotate-image")       
async def classify_with_annotated_image(file:UploadFile=File(...)):
    """Classify image and return annotated image with bounding boxes."""
    try:
        contents=await file.read()
        nparr=np.frombuffer(contents,np.uint8)
        image=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Could not decode image")
            
        # Convert to RGB for classification
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Perform classification
        result = ClassificationService.classify_image(image_rgb)
        
        #Draw ounding boxes on original image
        annotated_image=ClassificationService._draw_detections(image,result["detections"])
        
        #Encode annotated image 
        _,encoded_image=cv2.imencode('.jpg',annotated_image)
        image_bytes=encoded_image.tobytes()
        return StreamingResponse(
            io.BytesIO(image_bytes), 
            media_type="image/jpeg",
            headers={
                "X-Detection-Count": str(result["total_objects"]),
                "X-Processing-Time": f"{result['processing_time']:.3f}"
            }
        )
    except Exception as e :
        logger.error(f"Annotated image error: {e}")
        raise HTTPException(status_code=500, detail="Error generating annotated image")
        
