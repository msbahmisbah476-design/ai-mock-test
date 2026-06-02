import streamlit as st
import os
from supabase import create_client
from dotenv import load_dotenv
# Import the theme logic from your styles folder
from styles.themes import apply_selected_theme

# 1. Page Configuration (MUST be the first Streamlit command)
st.set_page_config(page_title="Login - AI Mock System", page_icon="🔐", layout="wide")

def set_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(to right, #0f2027, #203a43, #2b535e);
            color: #ffffff;
        }}
        [data-testid="stSidebar"] {{
            background-color: #1a1a1a !important;
            border-right: 2px solid #FFD700;
        }}
        .stButton>button {{
            background-color: #FFD700;
            color: black;
            border-radius: 10px;
            font-weight: bold;
            border: none;
        }}
        h1, h2, h3, p, label {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()
load_dotenv()

# 2. System Settings & Theme Toggle
with st.sidebar:
    st.title("⚙️ System Settings")
    theme_choice = st.select_slider("Select UI Theme", options=["Light", "Midnight Gold"])
    apply_selected_theme(theme_choice)

# 3. Database Connection (FIXED: No trailing slash or /rest/v1)
url = "https://jzvlgaobidpmxiyumfoa.supabase.co"
key = "sb_publishable_GmTw6TuUqdBmLzITq-HqyQ_jkbZceVT"
supabase = create_client(url, key)

# 4. Session State Management
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# 5. Security Layer: SQL Injection Protection
if st.session_state.user_email:
    if "'" in st.session_state.user_email or "--" in st.session_state.user_email:
        st.error("🚨 Security Alert: Malicious characters detected. Session locked.")
        st.session_state.user_email = None
        st.stop()

st.title("🔐 Student Registration & Login")

# 6. Main Login/Registration Logic
if not st.session_state.user_email:
    with st.form("user_details"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address (Unique ID)")
        mobile = st.text_input("Mobile Number")
        submit = st.form_submit_button("Start Analytics")

        if submit:
            if name and email and mobile:
                user_info = {"name": name, "email": email, "mobile": mobile}
                try:
                    # Sync to Supabase 'users' table
                    supabase.table("users").upsert(user_info, on_conflict="email").execute()
                    
                    # Update local state
                    st.session_state.user_email = email
                    st.session_state.user_name = name
                    st.success(f"Welcome {name}! Data synced to Cloud.")
                    st.rerun() # Refresh to show the 'logged in' view
                except Exception as e:
                    st.error(f"Database Sync Error: {e}")
            else:
                st.error("Please fill in all details to proceed.")
else:
    # 7. Post-Login View
    st.success(f"Successfully Logged in as: {st.session_state.user_name}")
    st.info("👈 Use the sidebar to navigate to the Dashboard or Take Test.")
    
    if st.button("Logout"):
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.rerun()