import streamlit as st
import pandas as pd

def show_detection_results(result, show_image=True):
    """Display detection results in a clean, minimal way"""
    
    if "annotated_image" in result:
        # Handle annotated image response
        st.subheader("🖼️ Results")
        
        # Show annotated image
        st.image(result["annotated_image"], use_container_width=True)
        
        # Simple metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Objects Found", result["detection_count"])
        with col2:
            st.metric("Processing Time", f"{result['processing_time']:.2f}s")
        
    else:
        # Handle regular classification response
        st.subheader("📊 Analysis Results")
        
        # Quick stats in a clean layout
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Objects", result["total_objects"])
        with col2:
            st.metric("Processing Time", f"{result['processing_time']:.2f}s")
        with col3:
            recyclable_count = sum(1 for det in result["detections"] 
                                 if det["waste_category"] == "recyclable")
            st.metric("Recyclable Items", recyclable_count)
        
        # Display detections in a clean table format
        if result["detections"]:
            show_detections_table(result["detections"])
            
            # Simple statistics
            show_simple_stats(result["detections"])
        else:
            st.info("🔍 No objects detected in the image")

def show_detections_table(detections):
    """Display detections in a clean table format"""
    st.subheader("📋 Detected Items")
    
    # Create a simple data table
    data = []
    for detection in detections:
        data.append({
            "Material": detection["class_name"].title(),
            "Category": detection["waste_category"].title(),
            "Confidence": f"{detection['confidence']:.1%}",
            "Score": detection["confidence"]  # For sorting
        })
    
    df = pd.DataFrame(data)
    
    # Display as a clean table without index
    st.dataframe(
        df[["Material", "Category", "Confidence"]],
        use_container_width=True,
        hide_index=True
    )

def show_simple_stats(detections):
    """Show simple statistics without complex charts"""
    st.subheader("📈 Quick Summary")
    
    # Basic counts
    df = pd.DataFrame(detections)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        unique_materials = df['class_name'].nunique()
        st.metric("Unique Materials", unique_materials)
    
    with col2:
        avg_confidence = df['confidence'].mean()
        st.metric("Avg Confidence", f"{avg_confidence:.1%}")
    
    with col3:
        high_conf_count = len(df[df['confidence'] > 0.8])
        st.metric("High Confidence", high_conf_count)
    
    # Material breakdown (simple text)
    st.write("**Material Breakdown:**")
    material_counts = df['class_name'].value_counts()
    for material, count in material_counts.items():
        st.write(f"• {material.title()}: {count} item(s)")
    
    # Recycling recommendations
    show_recycling_tips(detections)

def show_recycling_tips(detections):
    """Show practical recycling tips based on detected items"""
    st.subheader("♻️ Recycling Guidance")
    
    materials_present = set(det['class_name'].lower() for det in detections)
    
    tips = []
    
    if any(plastic in materials_present for plastic in ['plastic', 'pet', 'hdpe']):
        tips.append("**Plastic Items**: Rinse and check recycling symbols")
    
    if 'glass' in materials_present:
        tips.append("**Glass**: Separate by color if required in your area")
    
    if any(paper in materials_present for paper in ['paper', 'cardboard']):
        tips.append("**Paper/Cardboard**: Keep dry and flatten boxes")
    
    if 'metal' in materials_present:
        tips.append("**Metal**: Clean cans and remove labels")
    
    if 'biodegradable' in materials_present:
        tips.append("**Biodegradable**: Compost separately from recyclables")
    
    # General tips
    tips.append("**General**: Check local recycling guidelines for specific rules")
    tips.append("**When in doubt**: Throw it out to avoid contaminating recycling")
    
    for tip in tips:
        st.write(f"• {tip}")

# Alternative minimalist version with cards layout
def show_detection_results_cards(result):
    """Alternative: Display results as clean cards"""
    
    st.subheader("🔍 Detection Results")
    
    # Quick stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Objects Found", result["total_objects"])
    with col2:
        st.metric("Processing Time", f"{result['processing_time']:.2f}s")
    
    if not result["detections"]:
        st.info("No objects detected in the image")
        return
    
    # Display as cards
    st.subheader("📋 Detected Items")
    
    # Create columns for cards (2 or 3 per row depending on screen size)
    cols = st.columns(2)
    
    for i, detection in enumerate(result["detections"]):
        with cols[i % 2]:
            with st.container():
                st.markdown("---")
                
                # Material name and confidence
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"**{detection['class_name'].title()}**")
                with col_b:
                    confidence = detection['confidence']
                    color = "🟢" if confidence > 0.8 else "🟡" if confidence > 0.5 else "🔴"
                    st.write(f"{color} {confidence:.0%}")
                
                # Category
                category = detection["waste_category"]
                category_emoji = {
                    "recyclable": "♻️",
                    "biodegradable": "🌱",
                    "non_recyclable": "🚫"
                }.get(category, "📦")
                
                st.write(f"{category_emoji} {category.title()}")
                
                # Recycling tip if available
                if "recycling_tip" in detection:
                    with st.expander("💡 Tip"):
                        st.write(detection["recycling_tip"])

# Ultra-minimal version
def show_detection_results_minimal(result):
    """Ultra-minimal results display"""
    
    st.write("### 📊 Results")
    
    # Just the essential info
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Objects:** {result['total_objects']}")
    with col2:
        st.write(f"**Time:** {result['processing_time']:.2f}s")
    
    if result["detections"]:
        # Simple list
        st.write("**Detected:**")
        for detection in result["detections"]:
            emoji = {
                "recyclable": "♻️",
                "biodegradable": "🌱", 
                "non_recyclable": "🚫"
            }.get(detection["waste_category"], "📦")
            
            st.write(f"{emoji} {detection['class_name'].title()} ({detection['confidence']:.0%})")
    else:
        st.write("No objects detected")