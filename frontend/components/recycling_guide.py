import streamlit as st

def show_recycling_guide(api_client):
    """Display recycling guide information"""
    st.header("📚 Recycling Guide")
    
    guide_data = api_client.get_recycling_guide()
    
    if not guide_data:
        st.error("Could not load recycling guide")
        return
    
    guide = guide_data.get("guide", {})
    materials = guide.get("materials", [])
    general_tips = guide.get("general_tips", [])
    
    # Display materials information
    st.subheader("🗂️ Material Classification Guide")
    
    for material in materials:
        with st.expander(f"📦 {material['class_name']}", expanded=False):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                category = material['waste_category']
                color = {
                    'recyclable': 'green',
                    'biodegradable': 'orange',
                    'non_recyclable': 'red'
                }.get(category, 'gray')
                
                st.metric("Category", category.title())
            
            with col2:
                st.write("**Tips:**")
                st.write(material.get('recycling_tip', 'No specific tips available.'))
    
    # General tips
    st.subheader("💡 General Recycling Tips")
    for i, tip in enumerate(general_tips, 1):
        st.write(f"{i}. {tip}")