import streamlit as st
from PIL import Image

def image_upload_section():
    """Image upload section with drag and drop"""
    st.subheader("📤 Upload Image")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png', 'webp'],
        help="Upload an image containing garbage items"
    )
    
    return uploaded_file
