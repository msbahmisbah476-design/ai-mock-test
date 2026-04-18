import streamlit as st

# --- COMPLETE RESOURCE DATABASE ---
RECOMMENDATIONS = {
    "BCA (Computer Applications)": {
        "Channels": ["CodeWithHarry (Python/C)", "Jenny's Lectures (CS Fundamentals)", "BCA Expert", "Abdul Bari (Algorithms)"],
        "Courses": ["Coursera: Python for Everybody", "Udemy: Full Stack Web Dev", "Google Data Analytics Certificate"]
    },
    "B.Com (Commerce)": {
        "Channels": ["CA Parag Gupta (Accounts)", "Accounting Stuff", "Commerce Baba", "Economics on your tips"],
        "Courses": ["Swayam: Financial Accounting", "LinkedIn Learning: Advanced Excel for Business", "TallyPrime Certification"]
    },
    "BBA (Management)": {
        "Channels": ["Management Courses by Manoj", "Study.com Business", "Ekeeda Commerce", "Two Teachers"],
        "Courses": ["Google Project Management Certificate", "HubSpot Content Marketing", "Udemy: MBA in a Box"]
    },
    "PUC Science": {
        "Channels": ["PUC @ PARIKSHE SCIENCE (Kannada/English)", "Physics Wallah", "Khan Academy", "Unacademy NEET/JEE"],
        "Courses": ["BYJU'S Learning App", "KCET/NEET Mock Prep Series", "Diksha Karnataka Portal"]
    },
    "PUC Commerce": {
        "Channels": ["PUC @ PARIKSHE COMMERCE", "Rajiv Gandhi Classes", "Education point", "Commerce Coaching"],
        "Courses": ["CA Foundation Level 1 Prep", "Parikshe Sadhaka (Commerce Focus)", "Basic Statistics Course"]
    }
}

st.title("📅 Smart Study Planner")

# 1. DYNAMIC INPUT SECTION
with st.container():
    st.subheader("Set Your Study Target")
    col1, col2 = st.columns(2)
    
    with col1:
        # This dropdown controls the recommendations below
        course_type = st.selectbox("Select Your Stream:", list(RECOMMENDATIONS.keys()))
        subject = st.text_input("Subject You're Studying Today:")
    
    with col2:
        target_date = st.date_input("Target Completion Date")
        goal_type = st.selectbox("Goal Type:", ["Chapter Revision", "Mock Test", "Note Making", "Practical Lab"])

    if st.button("📌 Lock in My Goal"):
        st.success(f"Goal saved! You've committed to finishing {subject} by {target_date}. Let's go!")

st.divider()

# 2. THE DYNAMIC RECOMMENDATION ENGINE
# This section updates automatically based on 'course_type'
st.subheader(f"💡 Recommended Resources for {course_type}")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.markdown("#### 📺 Expert YouTube Channels")
    # We pull the list based on the user's selection above
    for channel in RECOMMENDATIONS[course_type]["Channels"]:
        st.info(f"🔗 {channel}")

with rec_col2:
    st.markdown("#### 🎓 Professional Online Courses")
    for course in RECOMMENDATIONS[course_type]["Courses"]:
        st.success(f"📝 {course}")

st.divider()

# 3. DAILY CHECKLIST
st.subheader("✅ Daily Study Discipline")
st.checkbox("Analyze last mock test score from Dashboard")
st.checkbox("Complete 10 MCQs from recommended channels")
st.checkbox("Write summary of today's learning")