from helpers.Settings import get_settings
import logging
from ultralytics import YOLO
import numpy as np
import cv2
from typing import List ,Optional
logger=logging.getLogger(__name__)


CLASS_NAMES: List[str] = [
        'BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC'
    ]

class GarbageClassifier:
    def __init__(self,model_path:Optional[str] = None):
        self.model_path=model_path
        self.model=None
        self.class_names=CLASS_NAMES
        self.load_model()
        
    def load_model(self):
        try:
            self.model=YOLO(self.model_path)
            #verify model matches our expected classes
            if hasattr(self.model,'names') and self.model.names:
                model_classes=list(self.model.names.values())
                if set(model_classes) != set(self.class_names):
                    logger.warning(f"Model Classes {model_classes} don't match expected {self.class_names}")
            
            #Warm up the model(preparation using dummy_input)
            dummy_input=np.random.randint(0,255,(get_settings.IMAGE_SIZE,get_settings.IMAGE_SIZE,3),dtype=np.uint8)
            _ = self.model(dummy_input,verbose=False)
            logger.info(f"Model loaded successfully for classes: {self.class_names}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
        
    def preprocess_image(self,image:np.ndarray)->np.ndarray:
        """
        Preprocess image for YOLO model with proper resizing 
        """
        original_h,original_w=image.shape[:2]
        resized=cv2.resize(image,(get_settings.IMAGE_SIZE,get_settings.IMAGE_SIZE))
        
        #convert to RGB and normalize
        if len(resized.shape) == 3:
            resized=cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
            
        normalized=resized.astype(np.float32) / 255.0
        return normalized
    
    def predict(self,image:np.ndarray):
        try:
            results=self.model(
                image,
                conf=get_settings.CONFIDENCE_THRESHOLD,
                iou=get_settings.IOU_THRESHOLD,
                imgsz=get_settings.IMAGE_SIZE,
                verbose=False
            )
            detections=[]
            for result in results:
                boxes=result.boxes
                if boxes is not None and len(boxes) >0:
                    for box in boxes:
                        class_id=int(box.cls.item())
                        class_name=self._get_class_name(class_id)
                        detection={
                            "class_id":class_id,
                            "class_name":class_name,
                            "confidence":float(box.conf.item()),
                            "bbox":{
                                "x1": float(box.xyxy[0][0]),
                                "y1": float(box.xyxy[0][1]),
                                "x2": float(box.xyxy[0][2]),
                                "y2": float(box.xyxy[0][3])
                            }
                        }
                        detections.append(detection)
            #sort by confidence 
            detections.sort(key= lambda x:x['confidence'],reverse=True)
            return detections
        except Exception as e:
            logger.error(f"Prediction error :{e}")
            return []
        
    def _get_class_name(self,class_id:int):
        
        if 0<= class_id <len(self.class_names):
            return self.class_names[class_id]
        return f"Unknown_{class_id}"
    
    
    
    
classifier=GarbageClassifier()