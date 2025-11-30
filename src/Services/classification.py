import logging
import numpy as np
import time
from models import classifier
from typing import List 
from helpers.constants import (
    WASTE_CATEGORY_MAPPING,
    RECYCLING_TIPS,
    WasteCategory
)
from Schemas import DetectionResult
import cv2
logger=logging.getLogger(__name__)

class ClassificationService:
    @staticmethod
    def classify_image(image:np.ndarray):
        start_time=time.time()
        
        #run prediction
        detections=classifier.predict(image)
        enhanced_detections = []
        for detection in detections:
            waste_category = WASTE_CATEGORY_MAPPING.get(
                detection["class_name"],
                WasteCategory.RECYCLABLE
            )
            recycling_tip=RECYCLING_TIPS.get(
                detection["class_name"],
                "Check local recycling guidelines."
            )
            enhanced_detection=DetectionResult(
                class_id=detection["class_id"],
                class_name=detection["class_name"],
                confidence=detection["confidence"],
                bbox=detection["bbox"],
                waste_category=waste_category,
                recycling_tip=recycling_tip
            )
            enhanced_detections.append(enhanced_detection)
            
        processing_time=time.time() -start_time
        
        #calculate waste statistics 
        waste_stats=ClassificationService._calculate_waste_statistics(enhanced_detections)
        
        return {
            "detections":enhanced_detections,
            "total_objects":len(enhanced_detections),
            "processing_time":processing_time,
            "image_size":{
                 "height": image.shape[0],
                "width": image.shape[1]
            },
            "waste_statistics":waste_stats,
            "recycling_recommendations":ClassificationService._get_recycling_recommandations(enhanced_detections)
            
            
        }    
        
    @staticmethod    
    def _calculate_waste_statistics(detections:List[DetectionResult]):
        """Calculate statistics about detected waste"""
        stats={
            "by_category":{},
            "by_material":{},
            "total_recyclable":0,
            "total_biodegradable":0,
            "total_non_recyclable":0
            
        }
        for detection in detections:
            #count by waste category
            category=detection.waste_category.value
            stats["by_category"][category]=stats["by_category"].get(category,0)+1
            #count by material
            material=detection.class_name
            stats["by_material"][material]=stats["by_material"].get(material,0)+1
            
            #update total
            if detection.waste_category == WasteCategory.RECYCLABLE:
                stats["total_recyclable"] += 1
            elif detection.waste_category == WasteCategory.BIODEGRADABLE:
                stats["total_biodegradable"] += 1
            else:
                stats["total_non_recyclable"] += 1
                
        return stats
    
    
    @staticmethod
    def _get_recycling_recommandations(detections:List[DetectionResult]):
        """Generate recycling recommendations based on detected items"""
        recommendations=[]
        materials=set(detection.class_name for detection in detections)
        if 'PLASTIC' in materials:
            recommendations.append("Separate plastics by type for better recycling efficiency.")
        
        if 'GLASS' in materials:
            recommendations.append("Handle glass carefully to avoid breakage and contamination.")
        
        if 'BIODEGRADABLE' in materials:
            recommendations.append("Compost biodegradable waste separately from recyclables.")
        
        if len(materials) > 3:
            recommendations.append("Consider using separate bins for different material types.")
            
        if not recommendations:
            recommendations.append("All detected materials appear to be properly sorted.")
        
        return recommendations
    
    @staticmethod
    def get_detailed_class_information():
        return classifier.get_class_info()
    
    
    @staticmethod
    def _draw_detections(image: np.ndarray, detections: list) -> np.ndarray:
        """
        Draw bounding boxes, class names, and confidence scores on the image.
        Args:
            image (np.ndarray): Original BGR image.
            detections (List[DetectionResult]): List of detection results.
        Returns:
            np.ndarray: Annotated image.
        """
        annotated_image = image.copy()

        for det in detections:
            # Convert bbox coordinates to integers
            x1, y1 = int(det.bbox.x1), int(det.bbox.y1)
            x2, y2 = int(det.bbox.x2), int(det.bbox.y2)

            # Choose color based on waste category
            if det.waste_category == WasteCategory.RECYCLABLE:
                color = (0, 255, 0)  # Green
            elif det.waste_category == WasteCategory.BIODEGRADABLE:
                color = (0, 165, 255)  # Orange
            else:
                color = (0, 0, 255)  # Red for non-recyclable

            # Draw bounding box
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)

            # Prepare label text
            label = f"{det.class_name} ({det.confidence*100:.1f}%)"

            # Calculate text size
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )

            # Draw filled rectangle behind text for readability
            cv2.rectangle(
                annotated_image,
                (x1, y1 - text_height - baseline),
                (x1 + text_width, y1),
                color,
                thickness=cv2.FILLED
            )

            # Put text on image
            cv2.putText(
                annotated_image,
                label,
                (x1, y1 - baseline),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),  # White text
                1,
                lineType=cv2.LINE_AA
            )

        return annotated_image
                
            
        
    