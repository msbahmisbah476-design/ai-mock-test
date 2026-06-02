import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from styles.themes import apply_selected_theme

# --- THEME & SECURITY ---
apply_selected_theme("Ocean Blue") # Teachers get a professional blue theme

# --- SECURITY LOCK: Set your admin email here ---
ADMIN_EMAIL = "msbahmisbah476@gmail.com" 

if "user_email" not in st.session_state or st.session_state.user_email != ADMIN_EMAIL:
    st.error("🚫 Access Denied: This portal is restricted to Faculty/Admin only.")
    st.stop()

# --- DATABASE CONNECTION ---
url = "https://jzvlgaobidpmxiyumfoa.supabase.co"
key = "sb_publishable_GmTw6TuUqdBmLzITq-HqyQ_jkbZceVT"
supabase = create_client(url, key)

st.title("👨‍🏫 Global Faculty Dashboard")
st.markdown("### *Real-time Institutional Analytics*")

# --- 1. FETCH ALL DATA ---
res = supabase.table("student_logs").select("*").execute()
all_data = pd.DataFrame(res.data)

if all_data.empty:
    st.warning("No student data available yet.")
else:
    # --- 2. GLOBAL METRICS ---
    total_students = all_data['email'].nunique()
    avg_score = all_data['score'].mean()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Students", total_students)
    m2.metric("Avg Class Score", f"{avg_score:.1f}%")
    m3.metric("Total Tests Taken", len(all_data))

    # --- 3. CLASS PERFORMANCE BY SUBJECT ---
    st.divider()
    st.subheader("📊 Subject-Wise Class Performance")
    
    # Box plot is professional for seeing score distribution
    fig = px.box(all_data, x="subject", y="score", 
                 points="all", color="subject",
                 title="Score Distribution across Subjects")
    st.plotly_chart(fig, use_container_width=True)

    # --- 4. TOP PERFORMERS TABLE ---
    st.divider()
    st.subheader("🏆 Top Achievers (All-Time)")
    leaderboard = all_data.groupby('email')['score'].max().sort_values(ascending=False).head(5)
    st.table(leaderboard)

    # --- 5. DATA EXPORT ---
    csv = all_data.to_csv(index=False).encode('utf-8')
    st.download_button("📂 Export Global Data (CSV)", csv, "global_report.csv", "text/csv")