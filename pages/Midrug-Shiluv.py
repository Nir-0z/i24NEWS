import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. הגדרת עמוד והזרקת ה-CSS ישירות לעמוד הנוכחי (שבירת הבידוד של סטרימליט)
st.set_page_config(layout="wide")

st.markdown("""
    <style>
        /* רקע אפור-עמוק מודרני */
        .stApp { 
            background-color: #f1f5f9 !important; 
        }
        
        /* כרטיסים לבנים בולטים עם פדינג ומרווח */
        div[data-testid="stVerticalBlockBorder"] {
            background-color: #ffffff !important;
            padding: 35px 40px !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05) !important;
            border: none !important;
            margin-bottom: 25px !important;
        }

        /* יישור גורף לימין וכיוון RTL קשיח */
        .stApp, .stApp * { 
            direction: rtl !important; 
            text-align: right !important; 
            font-family: 'Segoe UI', system-ui, sans-serif !important;
        }
        
        /* הכרחת התיבות הנפתחות (Dropdowns) להתיישר לימין */
        div[data-baseweb="select"] *, div[data-testid="stSelectbox"] * {
            text-align: right !important;
            direction: rtl !important;
        }
        div[data-testid="stSelectbox"] div {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* יישור כפתורי הרדיו של השאלות בצד ימין */
        div[data-testid="stRadio"] label {
            justify-content: flex-start !important;
            text-align: right !important;
            direction: rtl !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. טעינת נתונים
path = os.path.join(os.path.dirname(__file__), "השוואות.xlsx")
df_m = pd.read_excel(path, sheet_name="מדרוג", header=None)
df_s = pd.read_excel(path, sheet_name="שילוב", header=None)

questions = {str(r[0]): i for i, r in df_s.iterrows() if "q" in str(r[0]).lower() or ":" in str(r[0])}

cats = [str(x).strip() if pd.notna(x) else "" for x in df_s.iloc[0]]
for i in range(1, len(cats)): 
    if not cats[i]: cats[i] = cats[i-1]

demo = {"כללי": 3}
for idx in range(4, df_s.shape[1]):
    sub = df_s.iloc[1, idx]
    if pd.notna(sub): demo[f"{cats[idx]} - {str(sub).strip()}"] = idx

st.markdown("<h2 style='color: #0f172a; font-weight: 700; margin-bottom: 25px;'>📊 השוואת מדרוג מול סקר שילוב</h2>", unsafe_allow_html=True)

# 3. כרטיס פילטרים עליון
with st.container(border=True):
    col_f1, col_f2, _, _ = st.columns([1.2, 1.2, 1, 1])
    wave = col_f1.selectbox("גל מחקר", ["חיבור שניהם", "גל 19 במאי", "גל 25 במאי"])
    if wave == "חיבור שניהם":
        t_col = demo.get(col_f2.selectbox("פילוח דמוגרפי", list(demo.keys())), 3)
    else:
        t_col = 1 if wave == "גל 19 במאי" else 2

# 4. מבנה שני טורים (תפריט שאלות מימין, גרף משמאל)
col_side, col_chart = st.columns([1, 2.2], gap="large")

with col_side:
    with st.container(border=True):
        st.markdown("<p style='font-weight: 600; color: #475569; margin-bottom: 12px;'>בחר שאלה לניתוח</p>", unsafe_allow_html=True)
        sel_q = st.radio("", list(questions.keys()), label_visibility="collapsed")

with col_chart:
    with st.container(border=True):
        labels, s_vals, m_vals = [], [], []
        start_row = questions[sel_q] + 1
        
        for i in range(start_row, len(df_s)):
            row_s = df_s.iloc[i]
            if pd.isna(row_s[0]) or "q" in str(row_s[0]).lower(): 
                break
                
            txt = str(row_s[0]).lower().replace(" ", "")
            if "total" in txt or "סהכ" in txt or "מדגם" in txt: 
                continue
            
            row_m = df_m.iloc[i] if i < len(df_m) else [0.0]*10
            s_val = pd.to_numeric(row_s[t_col], errors='coerce')
            m_val = pd.to_numeric(row_m[t_col], errors='coerce')
            
            labels.append(str(row_s[0]))
            s_vals.append(float(s_val) if pd.notna(s_val) else 0.0)
            m_vals.append(float(m_val) if pd.notna(m_val) else 0.0)

        if not labels:
            st.info("לא נמצאו נתונים כמותיים להצגה עבור שאלה זו.")
        else:
            fig = go.Figure()
            
            # קווי קישור עדינים ברקע
            for lbl, s_v, m_v in zip(labels, s_vals, m_vals):
                if m_v > 0 or "עיקרי" not in sel_q:
                    fig.add_trace(go.Scatter(x=[m_v, s_v], y=[lbl, lbl], mode="lines", line=dict(color="#f1f5f9", width=6), hoverinfo="skip", showlegend=False))

            # סקר שילוב (כחול)
            fig.add_trace(go.Scatter(
                x=s_vals, y=labels, mode="markers+text", name='סקר שילוב', 
                marker=dict(color='#2563eb', size=13, line=dict(color='white', width=2)),
                text=[f"{x:.1f}%" for x in s_vals], textfont=dict(size=11, color="#2563eb", weight="bold"), 
                textposition="top center"
            ))
            
            # הוועדה למדרוג (כתום)
            fig.add_trace(go.Scatter(
                x=m_vals, y=labels, mode="markers+text", name='הוועדה למדרוג', 
                marker=dict(color='#f97316', size=13, line=dict(color='white', width=2)),
                text=[f"{x:.1f}%" if x > 0 else "" for x in m_vals], textfont=dict(size=11, color="#f97316", weight="bold"), 
                textposition="bottom center"
            ))

            fig.update_layout(
                margin=dict(l=50, r=280, t=50, b=70),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=500,
                legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center", font=dict(size=12, color="#475569")),
                xaxis=dict(showgrid=True, gridcolor="#f1f5f9", side="top", autorange="reversed", ticksuffix="%", tickfont=dict(size=11, color="#64748b")),
                yaxis=dict(autorange="reversed", side="right", tickfont=dict(size=13, color="#0f172a"), pad=25)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
