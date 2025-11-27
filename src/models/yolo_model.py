from helpers.Settings import get_settings
import logging
from ultralytics import YOLO
import numpy as np
logger=logging.getLogger(__name__)


CLASS_NAMES: List[str] = [
        'BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC'
    ]

class GarbageClassifier:
    def __init__(self,model_path:str):
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
        