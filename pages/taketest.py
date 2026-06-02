import streamlit as st
import requests
import random
import time
import pandas as pd
from supabase import create_client
import streamlit.components.v1 as components

# --- PAGE CONFIG & STYLES ---
def set_bg():
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(to right, #0f2027, #203a43, #2b535e); color: #ffffff; }
        [data-testid="stSidebar"] { background-color: #1a1a1a !important; border-right: 2px solid #FFD700; }
        .stButton>button { background-color: #FFD700; color: black; border-radius: 10px; font-weight: bold; border: none; }
        h1, h2, h3, p, label { color: white !important; }
        /* Style for correct/incorrect answers */
        .correct-box { padding: 15px; background-color: rgba(0, 255, 0, 0.15); border-left: 5px solid #00ff00; border-radius: 5px; margin-top: 10px; }
        .wrong-box { padding: 15px; background-color: rgba(255, 0, 0, 0.15); border-left: 5px solid #ff0000; border-radius: 5px; margin-top: 10px; }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# --- SECURITY GUARD ---
if "user_email" not in st.session_state or not st.session_state.user_email:
    st.warning("⚠️ Please login from the main page first.")
    st.stop()

# --- DATABASE CONNECTION ---
url = "https://jzvlgaobidpmxiyumfoa.supabase.co"
key = "sb_publishable_GmTw6TuUqdBmLzITq-HqyQ_jkbZceVT"
supabase = create_client(url, key)

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
with st.sidebar:
    st.header("⚙️ Test Setup")
    course = st.selectbox("Select Stream", list(UNIVERSITY_SYLLABUS.keys()))
    level = st.selectbox("Select Semester/Year", list(UNIVERSITY_SYLLABUS[course].keys()))
    sub_dict = UNIVERSITY_SYLLABUS[course][level]
    selected_sub = st.selectbox("Select Subject", list(sub_dict.keys()))
    st.divider()
    voice_cmd = st.text_input("🎙️ Voice Simulation", placeholder="Type 'Start' or 'Submit'")

# 2. START TEST LOGIC
if st.button("🚀 Start Mock Test") or voice_cmd.lower() == "start":
    st.session_state.start_time = time.time()
    st.session_state.current_course = f"{course} ({level})"
    st.session_state.submitted = False # Reset the submission state
    
    res = requests.get(f"https://opentdb.com/api.php?amount=10&category={sub_dict[selected_sub]}&type=multiple").json()
    if res['response_code'] == 0:
        st.session_state.quiz_data = res['results']
        st.session_state.current_sub = selected_sub
        # CRITICAL: Store randomized options so they don't change on rerun
        st.session_state.shuffled_options = [random.sample(q['incorrect_answers'] + [q['correct_answer']], 4) for q in res['results']]
        st.rerun()

# 3. QUIZ INTERFACE
if 'quiz_data' in st.session_state:
    st.write(f"### 📝 Testing: {st.session_state.current_sub}")
    
    user_ans = {}
    is_submitted = st.session_state.get('submitted', False)

    for i, q in enumerate(st.session_state.quiz_data):
        st.write(f"---")
        st.write(f"**Q{i+1}: {q['question']}**")
        
        # Display the question with options
        user_ans[i] = st.radio(
            f"Select option for Q{i+1}", 
            st.session_state.shuffled_options[i], 
            key=f"q{i}", 
            disabled=is_submitted # Lock choices after submission
        )

        # --- FEATURE: REVEAL ANSWERS ---
        if is_submitted:
            if user_ans[i] == q['correct_answer']:
                st.markdown(f'<div class="correct-box">✅ **Correct!** The answer is <b>{q["correct_answer"]}</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-box">❌ **Incorrect.** You selected {user_ans[i]}. The correct answer is <b>{q["correct_answer"]}</b></div>', unsafe_allow_html=True)

    # 4. SUBMISSION LOGIC
    if not is_submitted:
        if st.button("📝 Submit Results") or voice_cmd.lower() == "submit":
            correct_count = sum(1 for i, q in enumerate(st.session_state.quiz_data) if user_ans[i] == q['correct_answer'])
            score = int((correct_count / len(st.session_state.quiz_data)) * 100)
            duration = round((time.time() - st.session_state.start_time) / 60, 2)

            log_data = {
                "email": st.session_state.user_email,
                "course": st.session_state.current_course,
                "subject": st.session_state.current_sub,
                "score": score,
                "time_spent_mins": duration
            }
            
            try:
                supabase.table("student_logs").insert(log_data).execute()
                st.session_state.submitted = True # Set state to submitted
                st.success(f"Final Score: {score}%. Check the Review below!")
                st.rerun() # Refresh to trigger the Review Mode (is_submitted = True)
            except Exception as e:
                st.error(f"Database Error: {e}")
    else:
        if st.button("🔄 Take Another Test"):
            del st.session_state.quiz_data
            st.session_state.submitted = False
            st.rerun()