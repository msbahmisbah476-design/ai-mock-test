import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
from utils.master_logic import generate_pdf_marks_card, run_predictive_analysis, get_ai_weakness_analysis

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

# --- DATABASE CONNECTION ---
url = "https://jzvlgaobidpmxiyumfoa.supabase.co" 
key = "sb_publishable_GmTw6TuUqdBmLzITq-HqyQ_jkbZceVT"
supabase = create_client(url, key)

SEMESTER_MAP = {
    "BCA (Degree) - 1st Sem": ["C Programming", "Digital Electronics", "Discrete Maths", "English"],
    "BCA (Degree) - 2nd Sem": ["Data Structures", "DBMS", "Numerical Methods", "Environmental Science"],
    "BCA (Degree) - 3rd Sem": ["Java Programming", "Operating Systems", "Microprocessors", "Software Engineering"],
    "BCA (Degree) - 4th Sem": ["Python Programming", "Computer Networks", "Visual Programming", "Unix Shell"],
    "BCA (Degree) - 5th Sem": ["AI & ML", "Mobile Computing", "Cloud Computing", "Cyber Security"],
    "BCA (Degree) - 6th Sem": ["Data Science", "IoT", "Big Data", "Professional Ethics"],
    "B.Com (Degree) - 1st Sem": ["Financial Accounting", "Marketing", "Business Laws", "Management"],
    "B.Com (Degree) - 2nd Sem": ["Advanced Accounting", "Retail Management", "Business Math", "Banking"],
    "B.Com (Degree) - 3rd Sem": ["Corporate Accounting", "Income Tax", "Cost Accounting", "GST"],
    "B.Com (Degree) - 4th Sem": ["Advanced Corp Accounting", "E-Commerce", "Quant Techniques"],
    "B.Com (Degree) - 5th Sem": ["Audit & Assurance", "Management Accounting", "Business Stats"],
    "B.Com (Degree) - 6th Sem": ["Financial Management", "IFRS", "Principles of Management"],
    "BBA (Degree) - 1st Sem": ["Principles of Management", "Economics", "Accounting", "English"],
    "BBA (Degree) - 2nd Sem": ["Org Behavior", "Business Maths", "Marketing", "Communication"],
    "BBA (Degree) - 3rd Sem": ["HR Management", "Financial Management", "Business Analytics", "Soft Skills"],
    "BBA (Degree) - 4th Sem": ["Operations Management", "Entrepreneurship", "Research Methodology", "Ethics"],
    "BBA (Degree) - 5th Sem": ["Investment Management", "Strategic Management", "Consumer Behavior", "Taxation"],
    "BBA (Degree) - 6th Sem": ["Global Business", "Digital Marketing", "Project Management", "Viva"],
    "PUC Science - 1st Year": ["Physics", "Chemistry", "Maths", "Biology"],
    "PUC Science - 2nd Year": ["Physics", "Chemistry", "Maths", "Computer Science"],
    "PUC Commerce - 1st Year": ["Accountancy", "Business Studies", "Economics", "Statistics"],
    "PUC Commerce - 2nd Year": ["Accountancy", "Business Studies", "Economics", "Statistics"]
}

st.title("📊 Personalized Academic Dashboard")

# Security Check
if "user_email" not in st.session_state or not st.session_state.user_email:
    st.warning("⚠️ Please Login from the main page first!")
    st.stop()

# 1. Fetch data for the student
res = supabase.table("student_logs").select("*").eq("email", st.session_state.user_email).order('created_at', desc=True).execute()

if res.data:
    df = pd.DataFrame(res.data)
    latest = df.iloc[0]
    curr_ctx = latest['course']    
    curr_sub = latest['subject']   
    curr_score = latest['score']

    st.markdown(f"### 📍 Analysis for: **{curr_ctx}**")

    # --- FEATURE: ACHIEVEMENTS ---
    cols = st.columns(3)
    avg_score = df['score'].mean()
    if avg_score >= 80:
        cols[0].metric("Rank", "🏆 Gold Scholar")
    elif len(df) >= 3:
        cols[1].metric("Rank", "🥈 Silver Learner")
    else:
        cols[2].metric("Rank", "🥉 Beginner")

    # --- FEATURE: AI PERFORMANCE ANALYST ---
    st.divider()
    st.subheader("🤖 AI Performance Analyst")
    analysis_report = get_ai_weakness_analysis(df)
    st.info(analysis_report)
    
    # --- FEATURE 7: AI SUCCESS PREDICTION ---
    with st.expander("🔮 AI Future Score Prediction", expanded=False):
        prediction_msg = run_predictive_analysis(df)
        st.success(prediction_msg)

    # --- VISUALIZATION SECTION ---
    st.divider()
    v1, v2 = st.columns(2)
    
    with v1:
        st.subheader("📈 Syllabus Mastery")
        full_subject_list = SEMESTER_MAP.get(curr_ctx, [curr_sub])
        user_stats = df[df['course'] == curr_ctx].groupby('subject')['score'].mean().reset_index()
        final_df = pd.DataFrame({'subject': full_subject_list})
        final_df = final_df.merge(user_stats, on='subject', how='left').fillna(0)
        final_df['Color'] = ['#FFD700' if x == curr_sub else '#3498db' for x in final_df['subject']]

        fig = px.bar(final_df, x='subject', y='score', color='Color', color_discrete_map="identity")
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    with v2:
        st.subheader("🕸️ Skill Radar Chart")
        radar_data = df.groupby('subject')['score'].mean().reset_index()
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=radar_data['score'],
            theta=radar_data['subject'],
            fill='toself',
            line_color='#FFD700'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- FEATURE 9: 3D DATA VISUALIZATION ---
    st.divider()
    st.subheader("🧊 3D Multi-Dimensional Analytics")
    fig_3d = px.scatter_3d(df, x='subject', y='score', z='time_spent_mins',
                           color='score', size_max=18, opacity=0.7)
    st.plotly_chart(fig_3d, use_container_width=True)

    # --- IMPROVEMENT TIPS ---
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💡 Teacher's Advice")
        if curr_score >= 80:
            st.success(f"**Score: {curr_score}% (Distinction)**")
            msg, hours, note = "Excellent mastery!", "1 Hour", "🏆 You are making your parents proud."
        elif curr_score >= 50:
            st.warning(f"**Score: {curr_score}% (Average)**")
            msg, hours, note = "Good effort, more practice needed.", "3 Hours", "🌟 Success is near."
        else:
            st.error(f"**Score: {curr_score}% (Needs Attention)**")
            msg, hours, note = "Re-watch tutorials.", "5 Hours", "💪 Don't give up!"
        
        st.write(msg)

    with col2:
        st.subheader("⏰ Study Prescription")
        st.metric(f"Focus on {curr_sub}", f"{hours} / Day")
        st.markdown(f"**{note}**")
        
        st.write("---")
        st.subheader("📜 Official Documents")
        pdf_bytes = bytes(generate_pdf_marks_card(st.session_state.user_name, df))
        st.download_button(label="📥 Download Result (PDF)", 
                           data=pdf_bytes, 
                           file_name=f"{st.session_state.user_name}_Report.pdf",
                           mime="application/pdf")

else:
    st.warning("Please take a test first to generate your custom dashboard!")