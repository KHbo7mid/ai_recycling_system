import streamlit as st 
from PIL import Image
from utils import APIClient
from components import (show_header,image_upload_section,show_detection_results,batch_processing_section,show_recycling_guide)
st.set_page_config(
    page_title="AI Recycling System",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .detection-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .waste-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        margin: 2px;
    }
    .recyclable { background-color: #28a745; }
    .biodegradable { background-color: #ffc107; color: black; }
    .non-recyclable { background-color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)
    
def main():
    load_css()
    api_client = APIClient()
    st.sidebar.title("🗑️ Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose App Mode",
        ["🏠 Single Image Classification", "📊 Batch Processing", "📚 Recycling Guide"]
    )
    show_header()
    #check api health 
    if not api_client.check_health():
        st.error("🚨 Backend API is not available. Please make sure your server is running.")
        return 
    # Main application logic based on selected mode
    if app_mode == "🏠 Single Image Classification":
        single_image_classification(api_client)
    elif app_mode == "📊 Batch Processing":
        batch_processing_section(api_client)
    elif app_mode == "📚 Recycling Guide":
        show_recycling_guide(api_client)
    
    
def single_image_classification(api_client):
    st.header("🔍 Single Image Classification")
    
   
    uploaded_file=image_upload_section()
        
    if uploaded_file is not None:
        # Display uploaded image
        image=Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
            # Classification options
        
        get_annotated = st.checkbox("📷 Get Annotated Image", value=True)
        
            # Classify button
        if st.button("🚀 Classify Image", type="primary", use_container_width=True):
            with st.spinner("🔬 AI is analyzing the image..."):
                try:
                    # Perform classification
                    if get_annotated:
                        result = api_client.classify_with_annotated_image(uploaded_file)
                        if result:
                            show_detection_results(result, show_image=True)
                    else:
                        result = api_client.classify_image(uploaded_file)
                        if result:
                            show_detection_results(result, show_image=False)
                                
                except Exception as e:
                    st.error(f"❌ Classification failed: {str(e)}")
    
    
                
        
       
    
    

if __name__== "__main__":
    main()
    