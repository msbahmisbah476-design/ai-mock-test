import streamlit as st
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = "https://jzvlgaobidpmxiyumfoa.supabase.co"
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp6dmxnYW9iaWRwbXhpeXVtZm9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUxMjM0NDQsImV4cCI6MjA5MDY5OTQ0NH0.syIydrW4a5dnGUh3nB-Igp0WI3XlCOSYLvjcXC5zqos"
supabase = create_client(url, key)

st.set_page_config(page_title="Login - AI Mock System", page_icon="🔐")

# Session State to keep user logged in across pages
if "user_email" not in st.session_state:
    st.session_state.user_email = None

st.title("🔐 Student Registration & Login")
if not st.session_state.user_email:
    with st.form("user_details"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address (Unique ID)")
        mobile = st.text_input("Mobile Number")
        submit = st.form_submit_button("Start Analytics")

        if submit:
            if name and email and mobile:
                # Save to 'users' table in Supabase
                user_info = {"name": name, "email": email, "mobile": mobile}
                supabase.table("users").upsert(user_info, on_conflict="email").execute()
                
                st.session_state.user_email = email
                st.session_state.user_name = name
                st.success(f"Welcome {name}! Navigate to 'Dashboard' in the sidebar.")
            else:
                st.error("Please fill in all details to proceed.")
else:
    st.success(f"Logged in as: {st.session_state.user_name}")
    st.info("👈 Use the sidebar to view your Analytics or Study Planner.")