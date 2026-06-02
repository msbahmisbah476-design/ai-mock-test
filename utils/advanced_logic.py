import streamlit as st
from datetime import datetime

def analyze_sentiment(text):
    """
    Analyzes student feedback using Keyword-Based NLP logic.
    """
    text = text.lower()
    # Lexicon (Dictionary) of emotions
    positive = ['happy', 'confident', 'good', 'easy', 'great', 'prepared']
    negative = ['stressed', 'hard', 'difficult', 'confused', 'sad', 'scared']
    
    if any(word in text for word in positive):
        return "😊 **AI Insight:** Your confidence is a great asset. Maintain this mindset for the finals!"
    elif any(word in text for word in negative):
        return "🧘 **AI Insight:** It's normal to feel pressure. Why not try a 25-minute 'Study Sprint' now?"
    else:
        return "✍️ **AI Insight:** Keep pushing! Consistency is the key to mastering any subject."

def log_study_session(supabase, email, duration):
    """
    Saves a completed study sprint to the database.
    """
    try:
        data = {
            "email": email,
            "duration_mins": duration,
            "created_at": datetime.now().isoformat()
        }
        supabase.table("study_sessions").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error saving session: {e}")
        return False