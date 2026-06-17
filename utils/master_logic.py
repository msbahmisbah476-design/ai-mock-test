import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from fpdf import FPDF

def generate_pdf_marks_card(name, df):
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Page Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "AI MOCK TEST - ACADEMIC REPORT", ln=True, align='C')
    pdf.ln(10)
    
    # 2. Student Details
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Student Name: {name}", ln=True)
    pdf.cell(200, 10, f"Total Tests Taken: {len(df)}", ln=True)
    pdf.ln(5)
    
    # 3. Table Header
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(90, 10, "Subject", 1, 0, 'C', True)
    pdf.cell(60, 10, "Score (%)", 1, 1, 'C', True)
    
    # 4. Table Rows
    pdf.set_font("Arial", '', 12)
    for index, row in df.iterrows():
        pdf.cell(90, 10, str(row['subject']), 1)
        pdf.cell(60, 10, f"{row['score']}%", 1, 1, 'C')
        
    # 5. Output as a String Buffer
    # The 'latin-1' encoding is required for FPDF to output bytes correctly
    return bytes(pdf.output())

# 2. AI SUCCESS PREDICTION (Linear Regression)
def run_predictive_analysis(df):
    if len(df) < 2:
        return "Not enough data for a trend. Take more tests to see your prediction!"
    
    try:
        # Prepare data: X = Test Number, y = Score
        X = np.array(range(len(df))).reshape(-1, 1)
        y = df['score'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict the next test score
        next_index = np.array([[len(df)]])
        prediction = model.predict(next_index)[0]
        prediction = max(0, min(100, int(prediction))) # Keep between 0-100
        
        if prediction > 75:
            return f"🔮 Predicted Score: {prediction}% - You are on track for a Distinction!"
        else:
            return f"🔮 Predicted Score: {prediction}% - Focus more on revision to improve this trend."
    except:
        return "Analyzing your performance trends..."

# 3. AI WEAKNESS MAPPING LOGIC
def get_ai_weakness_analysis(df):
    if df is None or df.empty:
        return "⚠️ No test data found. Please complete a mock test to generate an analysis."
    
    # Calculate average score per subject
    subject_avg = df.groupby('subject')['score'].mean().reset_index()
    
    # Identify subjects where the student scored below 50%
    weak_areas = subject_avg[subject_avg['score'] < 50]['subject'].tolist()
    
    if not weak_areas:
        return "🌟 **AI Analysis:** Your performance is consistent across all subjects! No critical weak areas detected."
    
    # Generate the personalized feedback
    analysis = f"🤖 **AI Analyst:** Based on your last {len(df)} tests, I've identified that your performance in **{', '.join(weak_areas)}** is below the 50% threshold."
    analysis += "\n\n**Recommendation:** Revisit the core concepts of these subjects before your next attempt."
    
    return analysis