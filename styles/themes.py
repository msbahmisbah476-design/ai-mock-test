import streamlit as st

def apply_selected_theme(mode):
    if mode == "Midnight Gold":
        st.markdown("""
            <style>
            .stApp { background: #0f2027; color: #FFD700; }
            [data-testid="stSidebar"] { background-color: #1a1a1a !important; border-right: 2px solid #FFD700; }
            h1, h2, h3, p, label { color: #FFD700 !important; }
            .stButton>button { background-color: #FFD700; color: black; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp { background: #f0f2f6; color: #31333F; }
            [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 2px solid #3498db; }
            h1, h2, h3, p, label { color: #31333F !important; }
            .stButton>button { background-color: #3498db; color: white; }
            </style>
        """, unsafe_allow_html=True)