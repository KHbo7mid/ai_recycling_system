import streamlit as st
import pandas as pd
from PIL import Image
import io
import base64

def batch_processing_section(api_client):
    """Batch image processing interface"""
    st.header("📊 Batch Processing")
    
    uploaded_files = st.file_uploader(
        "Upload multiple images",
        type=['jpg', 'jpeg', 'png', 'webp'],
        accept_multiple_files=True,
        help="Select multiple images for batch classification"
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} images selected for processing")
        
        # Display uploaded images in a grid
        st.subheader("📸 Uploaded Images")
        cols = st.columns(4)
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i % 4]:
                image = Image.open(uploaded_file)
                st.image(image, caption=uploaded_file.name, use_container_width=True)
        
        if st.button("🚀 Process All Images", type="primary"):
            with st.spinner("🔬 Processing batch images..."):
                results = api_client.batch_classify(uploaded_files)
                
                if results:
                    show_batch_results(results, uploaded_files)

def show_batch_results(results, uploaded_files):
    """Display batch processing results with images"""
    successful = results["successful"]
    total = results["total_processed"]
    
    st.success(f"✅ Processed {successful}/{total} images successfully")
    
    # Create a mapping of filename to uploaded file for easy access
    file_map = {file.name: file for file in uploaded_files}
    
    # Summary statistics
    all_detections = []
    for result in results["results"]:
        if "result" in result and result["result"]:
            for detection in result["result"]["detections"]:
                detection["filename"] = result["filename"]
                all_detections.append(detection)
    
    if all_detections:
        df = pd.DataFrame(all_detections)
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Files", total)
        with col2:
            st.metric("Successful", successful)
        with col3:
            st.metric("Total Detections", len(all_detections))
        with col4:
            unique_classes = df['class_name'].nunique()
            st.metric("Unique Classes", unique_classes)
    
    # Detailed results with images
    st.subheader("📋 Classification Results")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["🎯 Image View", "📊 Summary View"])
    
    with tab1:
        # Display each image with its results
        for result in results["results"]:
            filename = result["filename"]
            
            # Create columns for image and results
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Display the original image
                if filename in file_map:
                    image = Image.open(file_map[filename])
                    st.image(image, caption=filename, use_container_width=True)
            
            with col2:
                if "result" in result and result["result"]:
                    detection_result = result["result"]
                    detections = detection_result["detections"]
                    
                    # Display file info
                    st.write(f"**File:** {filename}")
                    st.write(f"**Processing Time:** {detection_result['processing_time']:.2f}s")
                    st.write(f"**Objects Detected:** {detection_result['total_objects']}")
                    
                    if detections:
                        # Display detections in a nice format
                        for i, detection in enumerate(detections):
                            with st.container():
                                # Create badge for waste category
                                category = detection["waste_category"]
                                badge_color = {
                                    "recyclable": "🟢",
                                    "biodegradable": "🟡", 
                                    "non_recyclable": "🔴"
                                }.get(category, "⚪")
                                
                                # Display detection info
                                col_a, col_b, col_c = st.columns([3, 2, 1])
                                
                                with col_a:
                                    st.write(f"**{detection['class_name'].title()}**")
                                    st.write(f"{badge_color} {category.upper()}")
                                
                                with col_b:
                                    st.write(f"Confidence: {detection['confidence']:.1%}")
                                
                                with col_c:
                                    # Color code confidence score
                                    confidence = detection['confidence']
                                    if confidence > 0.8:
                                        color = "green"
                                    elif confidence > 0.5:
                                        color = "orange"
                                    else:
                                        color = "red"
                                    
                                    st.markdown(
                                        f"<h3 style='color: {color}; text-align: center;'>{confidence:.0%}</h3>", 
                                        unsafe_allow_html=True
                                    )
                                
                                # Recycling tip if available
                                if "recycling_tip" in detection and detection["recycling_tip"]:
                                    with st.expander("💡 Recycling Tip"):
                                        st.info(detection["recycling_tip"])
                                
                                st.divider()
                    else:
                        st.warning("❌ No objects detected in this image")
                else:
                    st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            
            st.markdown("---")  # Separator between images
    
    with tab2:
        # Summary statistics and analytics
        if all_detections:
            st.subheader("📈 Batch Analytics")
            
            # Create summary data
            summary_data = []
            for result in results["results"]:
                if "result" in result and result["result"]:
                    filename = result["filename"]
                    detections = result["result"]["detections"]
                    processing_time = result["result"]["processing_time"]
                    
                    summary_data.append({
                        "Filename": filename,
                        "Objects Detected": len(detections),
                        "Processing Time (s)": f"{processing_time:.2f}",
                        "Main Material": detections[0]["class_name"] if detections else "None",
                        "Highest Confidence": f"{max([d['confidence'] for d in detections]):.1%}" if detections else "N/A"
                    })
            
            # Display summary table
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True)
            
            # Material distribution chart
            st.subheader("🧩 Material Distribution Across All Images")
            
            if not df.empty:
                material_counts = df['class_name'].value_counts()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Bar chart
                    st.bar_chart(material_counts)
                
                with col2:
                    # Summary stats
                    st.write("**Detection Summary:**")
                    st.write(f"• Most common material: **{material_counts.index[0]}** ({material_counts.iloc[0]} detections)")
                    st.write(f"• Total unique materials: **{len(material_counts)}**")
                    
                    # Waste category breakdown
                    waste_counts = df['waste_category'].value_counts()
                    st.write("**Waste Categories:**")
                    for category, count in waste_counts.items():
                        st.write(f"• {category.title()}: **{count}** items")
            
            # Confidence analysis
            st.subheader("🎯 Confidence Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                avg_confidence = df['confidence'].mean()
                st.metric("Average Confidence", f"{avg_confidence:.1%}")
            
            with col2:
                high_confidence = len(df[df['confidence'] > 0.8])
                st.metric("High Confidence Detections", high_confidence)
        
        else:
            st.warning("No detections found in any of the processed images.")

def get_category_color(category):
    """Get color for waste category"""
    colors = {
        "recyclable": "#28a745",
        "biodegradable": "#ffc107", 
        "non_recyclable": "#dc3545"
    }
    return colors.get(category, "#6c757d")