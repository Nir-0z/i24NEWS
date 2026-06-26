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

# עיבוד נתונים מהיר
questions = {str(r[0]): i for i, r in df_s.iterrows() if "q" in str(r[0]).lower() or ":" in str(r[0])}
demo = {"כללי": 3} # קיצור לטובת הדוגמה (ניתן להוסיף את הלוגיקה המלאה מהקוד הקודם)

# --- כותרת ראשית ---
st.markdown("<h1 style='color: #1e293b; margin-bottom: 30px;'>📊 השוואת מדרוג מול סקר שילוב</h1>", unsafe_allow_html=True)

# --- כרטיס עליון: פילטרים ---
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
wave = c1.selectbox("בחירת גל מחקר", ["חיבור שניהם", "גל 19 במאי", "גל 25 במאי"])
t_col = 3 # ברירת מחדל לכללי
st.markdown('</div>', unsafe_allow_html=True)

# --- גוף הדשבורד ---
col_side, col_chart = st.columns([1, 2.5], gap="large")

with col_side:
    st.markdown('<div class="custom-card" style="height: 520px;">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 18px; color: #64748b;'>בחר שאלה לניתוח</h3>", unsafe_allow_html=True)
    sel_q = st.radio("", list(questions.keys()), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart:
    st.markdown('<div class="custom-card" style="height: 520px;">', unsafe_allow_html=True)
    
    # חילוץ נתונים (לוגיקה מקוצרת)
    labels, s_vals, m_vals = [], [], []
    for i in range(questions[sel_q] + 1, len(df_s)):
        row_s, row_m = df_s.iloc[i], df_m.iloc[i]
        if pd.isna(row_s[0]) or "q" in str(row_s[0]).lower(): break
        labels.append(str(row_s[0]))
        s_vals.append(pd.to_numeric(row_s[t_col], errors='coerce') or 0.0)
        m_vals.append(pd.to_numeric(row_m[t_col], errors='coerce') or 0.0)

    # יצירת הגרף המעוצב
    fig = go.Figure()
    
    # קווי הקישור (הדאמבל) - הפכנו אותם לעדינים מאוד
    for lbl, s_v, m_v in zip(labels, s_vals, m_vals):
        fig.add_trace(go.Scatter(x=[m_v, s_v], y=[lbl, lbl], mode="lines", line=dict(color="#f1f5f9", width=6), hoverinfo="skip", showlegend=False))

    # נקודות נתונים - צבעי פרימיום (כחול עמוק וכתום חיוני)
    fig.add_trace(go.Scatter(x=s_vals, y=labels, mode="markers+text", name='סקר שילוב', 
                             marker=dict(color='#2563eb', size=14, line=dict(color='white', width=2)),
                             text=[f"{x:.1f}%" for x in s_vals], textfont=dict(size=12, color="#2563eb"), textposition="top center"))
    
    fig.add_trace(go.Scatter(x=m_vals, y=labels, mode="markers+text", name='הוועדה למדרוג', 
                             marker=dict(color='#f97316', size=14, line=dict(color='white', width=2)),
                             text=[f"{x:.1f}%" if x > 0 else "" for x in m_vals], textfont=dict(size=12, color="#f97316"), textposition="bottom center"))

    # עיצוב פריסה (Layout) נקי
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=420,
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(size=13, color="#64748b")),
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9", side="top", autorange="reversed", ticksuffix="%"),
        yaxis=dict(autorange="reversed", side="right", tickfont=dict(size=13, color="#1e293b"))
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
