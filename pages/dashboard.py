import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

# --- DATABASE CONNECTION ---
url = "https://jzvlgaobidpmxiyumfoa.supabase.co"
key = "sb_publishable_GmTw6TuUqdBmLzITq-HqyQ_jkbZceVT"
supabase = create_client(url, key)

# --- THE MASTER SYLLABUS MAP (Matches your Take Test page) ---
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

# 1. Fetch data for the student
res = supabase.table("STUDENT_LOGS").select("*").eq("email", st.session_state.user_email).order('created_at', desc=True).execute()

if res.data:
    df = pd.DataFrame(res.data)
    
    # 2. Get the Context of the LATEST test (e.g., BBA 1st Sem)
    latest = df.iloc[0]
    curr_ctx = latest['course']    
    curr_sub = latest['subject']   
    curr_score = latest['score']

    st.markdown(f"### 📍 Analysis for: **{curr_ctx}**")

    # 3. Create the "FULL" subject list for the graph
    # This grabs the list from our map above
    full_subject_list = SEMESTER_MAP.get(curr_ctx, [curr_sub])
    
    # Calculate average scores for subjects actually taken
    user_stats = df[df['course'] == curr_ctx].groupby('subject')['score'].mean().reset_index()
    
    # Merge: This joins the 'Full Syllabus' with the 'User Results'
    # Any subject not yet taken will show as 0
    final_df = pd.DataFrame({'subject': full_subject_list})
    final_df = final_df.merge(user_stats, on='subject', how='left').fillna(0)

    # 4. COLOR CODING: Highlight current subject in GOLD, others in BLUE
    final_df['Color'] = ['#FFD700' if x == curr_sub else '#3498db' for x in final_df['subject']]

    # 5. RENDER BAR CHART
    fig = px.bar(final_df, x='subject', y='score', 
                 title=f"Full Syllabus Overview: {curr_ctx}",
                 color='Color', color_discrete_map="identity")
    
    # Set Y-axis to 100 so it looks like a real marks card
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    # 6. IMPROVEMENT TIPS & SWEET NOTE
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💡 Teacher's Advice")
        if curr_score >= 80:
            st.success(f"**Score: {curr_score}% (Distinction)**")
            msg = "Excellent! You have mastered this subject. Move to the next one."
            hours = "1 Hour"
            note = "🏆 **Sweet Note:** You are making your parents proud. Keep going!"
        elif curr_score >= 50:
            st.warning(f"**Score: {curr_score}% (Average)**")
            msg = "Good effort, but you need more practice with technical terms."
            hours = "3 Hours"
            note = "🌟 **Sweet Note:** You're doing great! Success is just around the corner."
        else:
            st.error(f"**Score: {curr_score}% (Needs Attention)**")
            msg = "Don't panic. Re-watch the basic tutorials and try again."
            hours = "5 Hours"
            note = "💪 **Sweet Note:** Don't give up! Every master was once a beginner."
        
        st.write(msg)

    with col2:
        st.subheader("⏰ Study Prescription")
        st.metric(f"Focus on {curr_sub}", f"{hours} / Day")
        st.markdown(f"**{note}**")

else:
    st.warning("Please take a test first to generate your custom dashboard!")