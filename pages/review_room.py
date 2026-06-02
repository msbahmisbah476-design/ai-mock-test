import streamlit as st
from supabase import create_client
from styles.themes import apply_selected_theme

# --- THEME & SECURITY ---
apply_selected_theme("Midnight Gold")

if "user_email" not in st.session_state:
    st.warning("⚠️ Please login to access your Review Room.")
    st.stop()


# --- DATABASE CONNECTION (Check these carefully!) ---
url = "https://jzvlgaobidpmxiyumfoa.supabase.co"
key = "sb_publishable_GmTw6TuUqdBmLzITq-HqyQ_jkbZceVT" # Use your actual long key here
supabase = create_client(url, key)

st.title("🎯 The AI Review Room")
st.markdown("##### *Master your mistakes to boost your score*")

# --- 1. FETCH WRONG ANSWERS ---
res = supabase.table("wrong_answers").select("*").eq("email", st.session_state.user_email).execute()
wrong_data = res.data

if not wrong_data:
    st.success("🎉 Incredible! You have no wrong answers to review. Keep it up!")
else:
    st.info(f"📚 You have {len(wrong_data)} concepts to review. Let's get to work!")
    
    # Organize by subject
    subjects = list(set([item['subject'] for item in wrong_data]))
    selected_sub = st.selectbox("Filter by Subject:", ["All"] + subjects)

    # --- 2. DISPLAY MISTAKES ---
    for item in wrong_data:
        if selected_sub == "All" or item['subject'] == selected_sub:
            with st.expander(f"📖 {item['subject']} | Question: {item['question'][:50]}..."):
                st.write(f"**Question:** {item['question']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.error(f"❌ Your Answer: {item['user_ans']}")
                with col2:
                    st.success(f"✅ Correct Answer: {item['correct_ans']}")
                
                st.write("---")
                st.caption("AI Tip: Re-read this specific topic in your textbook before your next mock test.")

# --- 3. CLEAR ROOM FEATURE ---
if st.sidebar.button("🗑️ Clear My Review Room"):
    supabase.table("wrong_answers").delete().eq("email", st.session_state.user_email).execute()
    st.sidebar.success("Room Cleared!")
    st.rerun()