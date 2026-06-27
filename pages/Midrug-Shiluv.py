import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. הגדרת עמוד
st.set_page_config(layout="wide", page_title="השוואת מדרוג ושילוב")

# 2. הזרקת CSS - הפעם העיצוב מכוון בדיוק לכרטיסיות ולתפריטים הפנימיים
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;800&display=swap');
        
        .stApp, .stApp * {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Assistant', sans-serif !important;
        }
        
        .stApp {
            background-color: #f0f2f6 !important;
        }
        
        /* עיצוב כרטיסיות מובנות של Streamlit (containers) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important;
            padding: 20px 25px !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
            border: 1px solid #e2e8f0 !important;
        }
        
        /* כותרת ראשית */
        h2 {
            color: #0f172a !important;
            font-weight: 800 !important;
            margin-bottom: 20px !important;
            padding-right: 15px;
        }
        
        /* מניעת עיצוב כפול בטורים עצמם */
        div[data-testid="column"] {
            background-color: transparent !important;
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* יישור קשיח של תיבות Selectbox ותפריטים נפתחים */
        div[data-baseweb="select"], div[data-baseweb="select"] > div {
            direction: rtl !important;
        }
        div[data-baseweb="popover"], ul[role="listbox"] {
            direction: rtl !important;
            text-align: right !important;
        }
        ul[role="listbox"] li {
            text-align: right !important;
            direction: rtl !important;
            padding-right: 15px !important;
        }
        
        /* עיצוב רשימת שאלות שתרגיש כמו תפריט בחירה רציף */
        div[data-testid="stRadio"] label {
            padding: 10px 15px !important;
            border-radius: 8px !important;
            background-color: transparent !important;
            margin-bottom: 4px !important;
            border: none !important;
            transition: background 0.2s ease;
        }
        div[data-testid="stRadio"] label:hover {
            background-color: #f1f5f9 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. טעינת הנתונים
try:
    path = os.path.join(os.path.dirname(__file__), "השוואות.xlsx")
    df_m = pd.read_excel(path, sheet_name="מדרוג", header=None)
    df_s = pd.read_excel(path, sheet_name="שילוב", header=None)
except Exception as e:
    st.error(f"שגיאה בטעינת הקובץ: {e}")
    st.stop()

questions = {str(r[0]): i for i, r in df_s.iterrows() if "q" in str(r[0]).lower() or ":" in str(r[0])}

if not questions:
    st.error("לא נמצאו שאלות תקינות בקובץ.")
    st.stop()

cats = [str(x).strip() if pd.notna(x) else "" for x in df_s.iloc[0]]
for i in range(1, len(cats)): 
    if not cats[i]: cats[i] = cats[i-1]

demo = {"כללי": 3}
for idx in range(4, df_s.shape[1]):
    sub = df_s.iloc[1, idx]
    if pd.notna(sub): demo[f"{cats[idx]} - {str(sub).strip()}"] = idx

st.markdown("<h2>📊 השוואת מדרוג מול סקר שילוב</h2>", unsafe_allow_html=True)

# =====================================================================
# 4. כרטיסיית הפילטרים - שימוש ב-3 טורים כדי למנוע מתיחה!
# =====================================================================
with st.container(border=True):
    st.markdown("<p style='font-weight: 700; color: #1e293b; margin-bottom: 5px;'>🎯 סינון נתונים</p>", unsafe_allow_html=True)
    # הטור השלישי (col_spacer) רחב יותר כדי "לדחוף" את הפילטרים ימינה ולא לתת להם להימתח
    col_f1, col_f2, col_spacer = st.columns([1.5, 1.5, 4])
    
    with col_f1:
        wave = st.selectbox("גל מחקר:", ["חיבור שניהם", "גל 19 במאי", "גל 25 במאי"])
    with col_f2:
        if wave == "חיבור שניהם":
            t_col = demo.get(st.selectbox("פילוח דמוגרפי:", list(demo.keys())), 3)
        else:
            t_col = 1 if wave == "גל 19 במאי" else 2

# חלוקה לטורים הראשיים
col_side, col_chart = st.columns([1.2, 2.5], gap="large")

# =====================================================================
# 5. כרטיסיית תפריט צד (ימין)
# =====================================================================
with col_side:
    with st.container(border=True):
        st.markdown("<p style='font-weight: 700; color: #334155; margin-bottom: 10px; padding-right:10px;'>📋 בחר שאלה לניתוח:</p>", unsafe_allow_html=True)
        sel_q = st.radio("", list(questions.keys()), label_visibility="collapsed")

# =====================================================================
# 6. כרטיסיית התרשים (שמאל)
# =====================================================================
with col_chart:
    with st.container(border=True):
        labels, s_vals, m_vals = [], [], []
        start_row = questions[sel_q] + 1
        
        for i in range(start_row, len(df_s)):
            row_s = df_s.iloc[i]
            if pd.isna(row_s[0]) or "q" in str(row_s[0]).lower(): 
                break
                
            txt = str(row_s[0]).lower().replace(" ", "")
            if any(x in txt for x in ["total", "סהכ", "מדגם"]): 
                continue
            
            s_val_raw = row_s[t_col] if t_col < len(row_s) else None
            m_val_raw = df_m.iloc[i, t_col] if i < len(df_m) and t_col < len(df_m.iloc[i]) else None
            
            s_val = pd.to_numeric(s_val_raw, errors='coerce')
            m_val = pd.to_numeric(m_val_raw, errors='coerce')
            
            labels.append(str(row_s[0]))
            s_vals.append(float(s_val) if pd.notna(s_val) else None)
            m_vals.append(float(m_val) if pd.notna(m_val) else None)

        if not labels or (all(x is None for x in s_vals) and all(x is None for x in m_vals)):
            st.info("לא נמצאו נתונים להצגה.")
        else:
            fig = go.Figure()
            
            for lbl, s_v, m_v in zip(labels, s_vals, m_vals):
                if s_v is not None and m_v is not None:
                    fig.add_trace(go.Scatter(
                        x=[m_v, s_v], y=[lbl, lbl], mode="lines", 
                        line=dict(color="#cbd5e1", width=2, dash="dot"), hoverinfo="skip", showlegend=False
                    ))

            fig.add_trace(go.Scatter(
                x=s_vals, y=labels, mode="markers+text", name='סקר שילוב', 
                marker=dict(color='#3b82f6', size=14, line=dict(color='white', width=3)),
                text=[f"<b>{x:.1f}%</b>" if x is not None else "" for x in s_vals], 
                textfont=dict(size=13, color="#2563eb", family="Assistant"), 
                textposition="top center"
            ))
            
            fig.add_trace(go.Scatter(
                x=m_vals, y=labels, mode="markers+text", name='הוועדה למדרוג', 
                marker=dict(color='#f97316', size=14, line=dict(color='white', width=3)),
                text=[f"<b>{x:.1f}%</b>" if x is not None else "" for x in m_vals], 
                textfont=dict(size=13, color="#ea580c", family="Assistant"), 
                textposition="bottom center"
            ))

            # --- מניעת הצגת מספרים שליליים בציר ה-X ויצירת מרווח נקי ---
            valid_vals = [v for v in s_vals + m_vals if v is not None]
            max_val = max(valid_vals) if valid_vals else 100
            
            # חישוב טווח דינמי ונקי
            safe_max = max_val + (max_val * 0.15) # אוויר בצד שמאל
            safe_min = -(max_val * 0.3) # משיכת הציר לתוך מינוס כדי ליצור רווח למילים
            
            # יצירת קפיצות נקיות לציר ה-X (למשל: 0, 5, 10...) כך שהמינוס לא יוצג כלל
            step = 5 if max_val <= 30 else 10
            clean_ticks = [i for i in range(0, int(safe_max) + step, step)]

            fig.update_layout(
                margin=dict(l=20, r=20, t=40, b=40), 
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=max(450, len(labels) * 55), 
                font=dict(family="Assistant"),
                
                legend=dict(
                    orientation="h", y=-0.1, x=0.5, xanchor="center", 
                    font=dict(size=14, color="#64748b")
                ),
                
                xaxis=dict(
                    range=[safe_max, safe_min],
                    tickvals=clean_ticks, # שימוש בערכים החיוביים בלבד שהגדרנו
                    showgrid=True, 
                    gridcolor="#f1f5f9", 
                    zeroline=False,
                    side="top",
                    ticksuffix="%", 
                    tickfont=dict(size=12, color="#94a3b8")
                ),
                
                yaxis=dict(
                    side="right", 
                    categoryorder="array",
                    categoryarray=labels[::-1], 
                    tickfont=dict(size=14, color="#334155", weight="bold"),
                    showgrid=False
                )
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
