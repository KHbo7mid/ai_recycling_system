import streamlit as st 

def show_header():
    """Display the application header"""
    st.markdown('<h1 class="main-header">AI Recycling System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.2rem; color: #666;'>
        AI-powered waste classification system that helps you sort garbage correctly for better recycling
        </p>
    </div>
    """, unsafe_allow_html=True)