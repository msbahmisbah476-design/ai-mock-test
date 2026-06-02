import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime, timedelta

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
        /* Styling for the attendance table text */
        .stTable td {{ color: black !important; font-weight: bold; text-align: center; }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# --- DATABASE CONNECTION ---
url = "https://jzvlgaobidpmxiyumfoa.supabase.co"
key = "sb_publishable_GmTw6TuUqdBmLzITq-HqyQ_jkbZceVT"
supabase = create_client(url, key)

# --- RESOURCE & TIPS DATABASE ---
RECOMMENDATIONS = {
    "BCA (Computer Applications)": {
        "Channels": ["CodeWithHarry", "Jenny's Lectures", "Abdul Bari"],
        "Courses": ["Coursera: Python", "Udemy: Full Stack Dev"]
    },
    "B.Com (Commerce)": {
        "Channels": ["CA Parag Gupta", "Accounting Stuff", "Commerce Baba"],
        "Courses": ["TallyPrime Certification", "Swayam: Accounting"]
    },
    "BBA (Management)": {
        "Channels": ["Management Courses by Manoj", "Two Teachers"],
        "Courses": ["Google Project Management", "MBA in a Box"]
    },
    "PUC Science": {
        "Channels": ["Physics Wallah", "Khan Academy", "Unacademy"],
        "Courses": ["BYJU'S Learning App", "KCET Mock Prep"]
    },
    "PUC Commerce": {
        "Channels": ["PUC @ PARIKSHE COMMERCE", "Education Point"],
        "Courses": ["CA Foundation Level 1", "Basic Statistics"]
    }
}

SUBJECT_TIPS = {
    "C Programming": "Focus on Pointers and Memory Management. Practice 'Linked Lists'.",
    "Python Programming": "Master List Comprehensions and Pandas for Data Analysis.",
    "Financial Accounting": "Ensure 'Balance Sheets' tally. Review the 'Golden Rules' daily.",
    "Physics": "Focus on Derivations and Numerical Problems. Use diagrams for visualizing.",
    "Computer Science": "Understand 'Boolean Algebra' and 'K-Maps' thoroughly."
}

st.title("📅 AI Smart Planner & Attendance")
def get_ai_summary(df):
    total = len(df)
    highest = df['score'].max()
    weak_sub = df[df['score'] < 50]['subject'].unique()
    
    summary = f"Hello! You have completed **{total}** mock tests so far. "
    summary += f"Your peak performance was **{highest}%**. "
    if len(weak_sub) > 0:
        summary += f"Our AI suggests prioritizing **{weak_sub[0]}** for your next session."
    return summary

if "user_email" not in st.session_state:
    st.warning("⚠️ Please Login from the main page first!")
    st.stop()

# --- 1. ATTENDANCE REGISTER LOGIC ---
st.subheader("📋 Student Attendance Register (Activity Based)")

res = supabase.table("student_logs").select("*").eq("email", st.session_state.user_email).execute()
df_logs = pd.DataFrame(res.data)

# Calculate active dates from Supabase
today = datetime.now()
date_list = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
active_dates = []
weak_subjects = []

if not df_logs.empty:
    active_dates = pd.to_datetime(df_logs['created_at']).dt.strftime('%Y-%m-%d').tolist()
    # Also find weak subjects for the timetable highlighting
    subj_avg = df_logs.groupby('subject')['score'].mean()
    weak_subjects = subj_avg[subj_avg < 50].index.tolist()

attendance_data = []
for d in date_list:
    status = "✅ PRESENT" if d in active_dates else "❌ ABSENT"
    attendance_data.append({"Date": d, "Status": status})

att_df = pd.DataFrame(attendance_data).set_index("Date").T

def color_att(val):
    color = '#2ecc71' if "PRESENT" in val else '#e74c3c'
    return f'background-color: {color}; color: white'

st.table(att_df.style.map(color_att))

# --- 2. WEEKLY STUDY GRID (ATTENDANCE STYLE) ---
st.divider()
st.subheader("🗓️ Weekly Study Schedule")

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
time_slots = ["09:00 AM", "02:00 PM", "07:00 PM"]

if 'timetable_data' not in st.session_state:
    st.session_state.timetable_data = {day: ["Free"] * len(time_slots) for day in days}

with st.expander("📝 Edit Your Study Register"):
    col1, col2, col3 = st.columns(3)
    d_sel = col1.selectbox("Day", days)
    t_sel = col2.selectbox("Time Slot", time_slots)
    # Suggest a weak subject if user has one
    suggest = weak_subjects[0] if weak_subjects else "General Revision"
    task = col3.text_input("Subject/Task", value=suggest)
    
    if st.button("Update Slot"):
        st.session_state.timetable_data[d_sel][time_slots.index(t_sel)] = task
        st.success("Slot Updated!")

sched_df = pd.DataFrame(st.session_state.timetable_data, index=time_slots)

def color_timetable(val):
    if val in weak_subjects:
        return 'background-color: #ff4b4b; color: white' # RED for weak subjects
    elif val != "Free":
        return 'background-color: #FFD700; color: black' # GOLD for others
    return 'color: gray'

st.table(sched_df.style.map(color_timetable))

# --- 3. DYNAMIC RESOURCE ENGINE & SUBJECT TIPS ---
st.divider()
st.subheader("💡 AI Recommendations")

c_col1, c_col2 = st.columns(2)
with c_col1:
    stream = st.selectbox("Select Stream:", list(RECOMMENDATIONS.keys()))
with c_col2:
    sub_query = st.text_input("Search Subject Advice:", placeholder="e.g. C Programming")

# Display Subject Tips
if sub_query:
    found = False
    for skey, stip in SUBJECT_TIPS.items():
        if sub_query.lower() in skey.lower():
            st.warning(f"🎯 **AI Pro-Tip for {skey}:** {stip}")
            found = True
            break
    if not found:
        st.info("💡 Keep studying! Consistency is the key to mastery.")

# Display Resources
rcol1, rcol2 = st.columns(2)
with rcol1:
    st.markdown("#### 📺 Channels")
    for ch in RECOMMENDATIONS[stream]["Channels"]:
        st.info(f"🔗 {ch}")
with rcol2:
    st.markdown("#### 🎓 Courses")
    for co in RECOMMENDATIONS[stream]["Courses"]:
        st.success(f"📝 {co}")

# --- 4. DISCIPLINE CHECKLIST ---
st.divider()
st.subheader("✅ Daily Study Checklist")
st.checkbox("Analyze Mock Test scores")
if today.strftime('%Y-%m-%d') in active_dates:
    st.success("✨ Attendance Marked for today!")
else:
    st.error("❗ Take a test today to mark your attendance!")
st.checkbox("Complete 10-minute focus sprint")