import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from main import set_rtl

st.set_page_config(layout="wide")
set_rtl()

# טעינת נתונים
path = os.path.join(os.path.dirname(__file__), "השוואות.xlsx")
df_m = pd.read_excel(path, sheet_name="מדרוג", header=None)
df_s = pd.read_excel(path, sheet_name="שילוב", header=None)

# מיפוי שאלות
questions = {str(r[0]): i for i, r in df_s.iterrows() if "q" in str(r[0]).lower() or ":" in str(r[0])}

# בניית פילטר דמוגרפיות
cats = [str(x).strip() if pd.notna(x) else "" for x in df_s.iloc[0]]
for i in range(1, len(cats)): 
    if not cats[i]: cats[i] = cats[i-1]

demo = {"כללי": 3}
for idx in range(4, df_s.shape[1]):
    sub = df_s.iloc[1, idx]
    if pd.notna(sub): demo[f"{cats[idx]} - {str(sub).strip()}"] = idx

st.markdown("<h2 style='color: #0f172a; font-weight: 700; margin-bottom: 25px;'>📊 השוואת מדרוג מול סקר שילוב</h2>", unsafe_allow_html=True)

# פילטרים
with st.container(border=True):
    col_f1, col_f2, _, _ = st.columns([1.2, 1.2, 1, 1])
    wave = col_f1.selectbox("גל מחקר", ["חיבור שניהם", "גל 19 במאי", "גל 25 במאי"])
    
    # הגנה קשיחה על בחירת עמודת הדמוגרפיה
    if wave == "חיבור שניהם":
        selected_demo = col_f2.selectbox("פילוח דמוגרפי", list(demo.keys()))
        t_col = demo.get(selected_demo, 3) # אם לא נמצא, יחזור כברירת מחדל ל'כללי' (עמודה 3)
    else:
        t_col = 1 if wave == "גל 19 במאי" else 2

col_side, col_chart = st.columns([1, 2.2], gap="large")

with col_side:
    with st.container(border=True):
        st.markdown("<p style='font-weight: 600; color: #475569; margin-bottom: 12px;'>בחר שאלה לניתוח</p>", unsafe_allow_html=True)
        sel_q = st.radio("", list(questions.keys()), label_visibility="collapsed")

with col_chart:
    with st.container(border=True):
        
        labels, s_vals, m_vals = [], [], []
        start_row = questions[sel_q] + 1
        
        # הגדרת גבול ריצה מקסימלי לפי הגיליון הקצר מבין השניים למניעת קריסת אינדקס
        max_rows = min(len(df_s), len(df_m))
        
        for i in range(start_row, max_rows):
            try:
                row_s = df_s.iloc[i]
                row_m = df_m.iloc[i]
                
                # עצירה אם הגענו לשאלה הבאה או לשורה ריקה לחלוטין
                if pd.isna(row_s[0]) or "q" in str(row_s[0]).lower(): 
                    break
                
                txt = str(row_s[0]).lower().replace(" ", "")
                if "total" in txt or "סהכ" in txt or "מדגם" in txt: 
                    continue
                
                # חילוץ ערכים עם המרה בטוחה למספרים
                s_val = pd.to_numeric(row_s[t_col], errors='coerce')
                m_val = pd.to_numeric(row_m[t_col], errors='coerce')
                
                # החלפת ערכי NaN באפסים בצורה בטוחה
                s_val = float(s_val) if pd.notna(s_val) else 0.0
                m_val = float(m_val) if pd.notna(m_val) else 0.0
                
                labels.append(str(row_s[0]))
                s_vals.append(s_val)
                m_vals.append(m_val)
                
            except Exception:
                # במקרה של שורה פגומה ספציפית - דלג עליה והמשך בריצה מבלי להקריס את האפליקציה
                continue

        # הצגת הגרף רק אם קיימים נתונים תקפים
        if not labels or len(s_vals) == 0:
            st.info("אין נתונים כמותיים להצגה עבור שאלה זו בפילוח שנבחר.")
        else:
            fig = go.Figure()
            
            # קווי קישור רק
