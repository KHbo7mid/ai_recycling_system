from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import List
from Schemas import BatchClassificationResponse, BatchClassificationResult
from .classification import classify_image
import logging

logger = logging.getLogger(__name__)

batch_router = APIRouter(
    prefix="/api",
    tags=["batch_classification"]
)

@batch_router.post("/batch_classify", response_model=BatchClassificationResponse)
async def batch_classify(files: List[UploadFile] = File(...), limit: int = 20):
    """Classify multiple images with batch processing"""
    
    if len(files) > limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {limit} images allowed per batch"
        )

    results = []
    successful = 0
    failed = 0

    for file in files:
        try:
            
            result = await classify_image(file)

            results.append(BatchClassificationResult(
                filename=file.filename,
                result=result
            ))
            successful += 1

        except Exception as e:
            logger.error(f"Batch processing error for {file.filename}: {e}")
            results.append(BatchClassificationResult(
                filename=file.filename,
                error=str(e)
            ))
            failed += 1

    return BatchClassificationResponse(
        results=results,
        total_processed=len(files),
        successful=successful,
        failed=failed
    )
