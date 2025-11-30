from pydantic import BaseModel
from typing import Optional,List
from .classificationResponse import ClassificationResponse

class BatchClassificationResult(BaseModel):
    filename: Optional[str]
    result: Optional[ClassificationResponse] = None
    error: Optional[str] = None

class BatchClassificationResponse(BaseModel):
    results: List[BatchClassificationResult]
    total_processed: int
    successful: int
    failed: int