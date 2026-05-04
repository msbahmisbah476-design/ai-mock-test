import streamlit as st
import requests
import random
import time
import pandas as pd
from supabase import create_client
def set_bg():
    st.markdown(
        f"""
        <style>
        /* Main background gradient */
        .stApp {{
            background: linear-gradient(to right, #0f2027, #203a43, #2b535e);
            color: #ffffff;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: #1a1a1a !important;
            border-right: 2px solid #FFD700;
        }}

        /* Gold Button styling */
        .stButton>button {{
            background-color: #FFD700;
            color: black;
            border-radius: 10px;
            font-weight: bold;
            border: none;
        }}
        
        /* Ensure text is visible on dark background */
        h1, h2, h3, p, label {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True  # Corrected parameter name
    )

set_bg()
# --- DATABASE CONNECTION ---
url = "https://jzvlgaobidpmxiyumfoa.supabase.co"
key = "sb_publishable_GmTw6TuUqdBmLzITq-HqyQ_jkbZceVT" 
supabase = create_client(url, key)

# --- THE MEGA SYLLABUS ---
UNIVERSITY_SYLLABUS = {
    "BCA (Computer Applications)": {
        "1st Sem": {"C Programming": 18, "Digital Electronics": 18, "Discrete Maths": 19},
        "2nd Sem": {"Data Structures": 18, "DBMS": 18, "Numerical Methods": 19},
        "3rd Sem": {"Java Programming": 18, "Operating Systems": 18, "Software Engineering": 18},
        "4th Sem": {"Python Programming": 18, "Computer Networks": 18, "Unix Shell": 18},
        "5th Sem": {"AI & ML": 18, "Mobile Computing": 18, "Cloud Computing": 18},
        "6th Sem": {"Data Science": 18, "IoT": 18, "Cyber Security": 18}
    },
    "B.Com (Commerce)": {
        "1st Sem": {"Financial Accounting": 19, "Marketing": 9},
        "2nd Sem": {"Advanced Accounting": 19, "Banking": 19},
        "3rd Sem": {"Corporate Accounting": 19, "Cost Accounting": 19},
        "4th Sem": {"GST Law": 19, "E-Commerce": 19},
        "5th Sem": {"Audit": 19, "Business Stats": 19},
        "6th Sem": {"Financial Management": 19, "Management Principles": 9}
    },
    "BBA (Management)": {
        "1st Sem": {"Management Principles": 9, "Accounting": 19},
        "2nd Sem": {"Business Maths": 19, "Marketing": 9},
        "3rd Sem": {"HR Management": 9, "Finance": 19},
        "4th Sem": {"Operations": 9, "Research": 9},
        "5th Sem": {"Investment": 19, "Strategy": 9},
        "6th Sem": {"Global Business": 9, "Digital Marketing": 9}
    },
    "PUC Science": {
        "1st Year": {"Physics": 17, "Chemistry": 17, "Maths": 19, "Biology": 17},
        "2nd Year": {"Physics": 17, "Chemistry": 17, "Maths": 19, "Computer Science": 18}
    },
    "PUC Commerce": {
        "1st Year": {"Accountancy": 19, "Business Studies": 9, "Economics": 9, "Statistics": 19},
        "2nd Year": {"Accountancy": 19, "Business Studies": 9, "Economics": 9, "Statistics": 19}
    }
}

st.title("🏛️ AI Mock Test Portal")

# 1. SELECTION UI
course = st.selectbox("Select Stream", list(UNIVERSITY_SYLLABUS.keys()))
level = st.selectbox("Select Semester/Year", list(UNIVERSITY_SYLLABUS[course].keys()))
sub_dict = UNIVERSITY_SYLLABUS[course][level]
selected_sub = st.selectbox("Select Subject", list(sub_dict.keys()))

# 2. START TEST LOGIC
if st.button("🚀 Start Mock Test"):
    # Reset and Start Clock
    st.session_state.start_time = time.time()
    st.session_state.current_course = f"{course} ({level})"
    
    # Fetch 10 questions
    res = requests.get(f"https://opentdb.com/api.php?amount=10&category={sub_dict[selected_sub]}&type=multiple").json()
    if res['response_code'] == 0:
        st.session_state.quiz_data = res['results']
        st.session_state.current_sub = selected_sub
        st.rerun()

# 3. QUIZ INTERFACE WITH TIMER
if 'quiz_data' in st.session_state:
    
    # --- TIMER LOGIC START ---
    time_limit = 10 * 60 # 10 Minutes
    elapsed = time.time() - st.session_state.get('start_time', time.time())
    remaining = time_limit - elapsed

    with st.sidebar:
        st.markdown("## ⏳ Time Remaining")
        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            st.subheader(f"⏱️ {mins:02d}:{secs:02d}")
            if remaining < 60:
                st.warning("⚠️ Hurry up! One minute left!")
        else:
            st.error("⏰ TIME EXPIRED!")
            st.write("Please click submit to save your progress.")
    # --- TIMER LOGIC END ---

    st.write(f"### 📝 Testing: {st.session_state.current_sub}")
    
    user_ans = {}
    for i, q in enumerate(st.session_state.quiz_data):
        st.write(f"**Q{i+1}: {q['question']}**")
        opts = random.sample(q['incorrect_answers'] + [q['correct_answer']], 4)
        user_ans[i] = st.radio(f"Select option for Q{i+1}", opts, key=f"q{i}")

    if st.button("📝 Submit Results"):
        # Calculate Stats
        correct = sum(1 for i, q in enumerate(st.session_state.quiz_data) if user_ans[i] == q['correct_answer'])
        score = int((correct / len(st.session_state.quiz_data)) * 100)
        duration = round((time.time() - st.session_state.start_time) / 60, 2)

        # --- NEW EMOJI & ANIMATION LOGIC ---
        if score >= 80:
            st.balloons() # This triggers the balloon animation
            st.success(f"🥳 **Amazing Work!** You got {correct} out of 10 correct! ({score}%)")
            st.markdown("### 😍 Keep it up, you're a genius!")
        
        elif score >= 50:
            st.info(f"🙂 **Good Effort!** You got {correct} out of 10 correct! ({score}%)")
            st.markdown("### ✨ You're doing well! Just a little more practice.")
        
        else:
            st.error(f"😟 **Don't be sad!** You got {correct} out of 10 correct. ({score}%)")
            st.markdown("### 📚 Try again! Every mistake makes you smarter.")
        
        # --- SAVE TO SUPABASE (Keep your existing code) ---
        log_data = {
            "email": st.session_state.user_email,
            "course": st.session_state.current_course,
            "subject": st.session_state.current_sub,
            "score": score,
            "time_spent_mins": duration,
            "created_at": pd.Timestamp.now(tz='UTC').isoformat()
        }
        
        try:
            supabase.table("STUDENT_LOGS").insert(log_data).execute()
            del st.session_state.quiz_data # Clear test after showing result
        except Exception as e:
            st.error(f"Save Error: {e}")