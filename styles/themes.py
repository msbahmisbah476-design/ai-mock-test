import streamlit as st

def apply_selected_theme(mode):
    if mode == "Midnight Gold":
        st.markdown("""
            <style>
            .stApp { 
                background: linear-gradient(to right, #0f2027, #203a43, #2b535e); 
                color: #ffffff; 
            }
            [data-testid="stSidebar"] { 
                background-color: #1a1a1a !important; 
                border-right: 2px solid #FFD700; 
            }
            h1, h2, h3, h4, p, label { color: #FFD700 !important; }
            .stButton>button { 
                background-color: #FFD700; 
                color: black; 
                border-radius: 10px;
                font-weight: bold;
            }
            /* Styling for metrics in dark mode */
            [data-testid="stMetricValue"] { color: #FFD700 !important; }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Light Mode: Ocean Blue
        st.markdown("""
            <style>
            .stApp { 
                background: #f0f2f6; 
                color: #31333F; 
            }
            [data-testid="stSidebar"] { 
                background-color: #ffffff !important; 
                border-right: 2px solid #3498db; 
            }
            h1, h2, h3, h4, p, label { color: #1f77b4 !important; }
            .stButton>button { 
                background-color: #3498db; 
                color: white; 
                border-radius: 10px;
            }
            /* Styling for metrics in light mode */
            [data-testid="stMetricValue"] { color: #3498db !important; }
            </style>
        """, unsafe_allow_html=True)