import requests
import streamlit as st 
from PIL import Image
import io 
import base64

class APIClient:
    def __init__(self,api_url="http://localhost:8000/api"):
        self.api_url=api_url
        
    def check_health(self):
        try:
            response=requests.get(f"{self.api_url}/health",timeout=5)
            return response.status_code==200
        except:
            return False
        
        
    def classify_image(self, uploaded_file):
        """Classify a single image"""
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(f"{self.api_url}/classify", files=files)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                return None
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
            return None
        
        
    def classify_with_annotated_image(self, uploaded_file):
        """Classify and get annotated image"""
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(f"{self.api_url}/classify/annotate-image", files=files)
            
            if response.status_code == 200:
                # For annotated images, we need to handle both image and data
                annotated_image = Image.open(io.BytesIO(response.content))
                
                # Get detection info from headers
                detection_count = response.headers.get("X-Detection-Count", 0)
                processing_time = response.headers.get("X-Processing-Time", 0)
                
                return {
                    "annotated_image": annotated_image,
                    "detection_count": int(detection_count),
                    "processing_time": float(processing_time),
                    "image_data": response.content
                }
            else:
                st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                return None
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
            return None
        
    def batch_classify(self, uploaded_files):
        """Classify multiple images"""
        try:
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            response = requests.post(f"{self.api_url}/batch_classify", files=files)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                return None
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
            return None
    
    def get_recycling_guide(self):
        """Get recycling guide information"""
        try:
            response = requests.get(f"{self.api_url}/recycling-guide")
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def get_classes_info(self):
        """Get information about all classes"""
        try:
            response = requests.get(f"{self.api_url}/classes")
            return response.json() if response.status_code == 200 else None
        except:
            return None