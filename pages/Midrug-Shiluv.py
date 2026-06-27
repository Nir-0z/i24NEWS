import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. הגדרת עמוד
st.set_page_config(layout="wide", page_title="השוואת מדרוג ושילוב")

# 2. הזרקת CSS מתקדם - יצירת כרטיסיות נפרדות לכל טור ויישור מוחלט
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
        
        /* הפיכת כל טור (Column) לכרטיסייה נפרדת ולבנה */
        div[data-testid="column"] {
            background-color: #ffffff !important;
            padding: 30px 25px !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
            border: 1px solid #e2e8f0 !important;
            margin-bottom: 20px !important;
        }
        
        /* כותרת ראשית */
        h2 {
            color: #0f172a !important;
            font-weight: 800 !important;
            margin-bottom: 30px !important;
            padding-right: 15px;
        }
        
        /* --- תיקון אגרסיבי לתפריטים נפתחים (Selectbox) --- */
        div[data-baseweb="select"], div[data-baseweb="select"] > div {
            direction: rtl !important;
        }
        /* התפריט הצף עצמו (Popover) */
        div[data-baseweb="popover"], ul[role="listbox"] {
            direction: rtl !important;
            text-align: right !important;
        }
        /* פריטי הרשימה בתוך התפריט */
        ul[role="listbox"] li {
            text-align: right !important;
            direction: rtl !important;
            padding-right: 15px !important;
        }
        
        /* עיצוב רדיו כפתורים */
        div[data-testid="stRadio"] label {
            padding: 10px !important;
            border-radius: 8px !important;
            background-color: #f8fafc !important;
            margin-bottom: 8px !important;
            border: 1px solid #f1f5f9;
        }
        div[data-testid="stRadio"] label:hover {
            background-color: #e2e8f0 !important;
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

# מיפוי השאלות
questions = {str(r[0]): i for i, r in df_s.iterrows() if "q" in str(r[0]).lower() or ":" in str(r[0])}

if not questions:
    st.error("לא נמצאו שאלות תקינות בקובץ.")
    st.stop()

# פילוח דמוגרפי דינמי
cats = [str(x).strip() if pd.notna(x) else "" for x in df_s.iloc[0]]
for i in range(1, len(cats)): 
    if not cats[i]: cats[i] = cats[i-1]

demo = {"כללי": 3}
for idx in range(4, df_s.shape[1]):
    sub = df_s.iloc[1, idx]
    if pd.notna(sub): demo[f"{cats[idx]} - {str(sub).strip()}"] = idx

st.markdown("<h2>📊 השוואת מדרוג מול סקר שילוב</h2>", unsafe_allow_html=True)

# 4. חלוקה לטורים עבור פילטרים עליונים
col_f1, col_f2 = st.columns(2)
with col_f1:
    wave = st.selectbox("גל מחקר:", ["חיבור שניהם", "גל 19 במאי", "גל 25 במאי"])
with col_f2:
    if wave == "חיבור שניהם":
        t_col = demo.get(st.selectbox("פילוח דמוגרפי:", list(demo.keys())), 3)
    else:
        t_col = 1 if wave == "גל 19 במאי" else 2

# 5. חלוקת המבנה לטורים מרכזיים (ההפרדה לכרטיסיות קורית כאן בזכות ה-CSS החדש)
col_side, col_chart = st.columns([1.2, 2.5], gap="large")

with col_side:
    st.markdown("<p style='font-weight: 700; color: #334155;'>בחר שאלה לניתוח:</p>", unsafe_allow_html=True)
    sel_q = st.radio("", list(questions.keys()), label_visibility="collapsed")

with col_chart:
    labels, s_vals, m_vals = [], [], []
    start_row = questions[sel_q] + 1
    
    # חילוץ הנתונים
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

        # --- חישוב דינמי כדי למנוע חפיפה של הטקסט על ציר ה-Y ---
        valid_vals = [v for v in s_vals + m_vals if v is not None]
        max_val = max(valid_vals) if valid_vals else 100
        min_val = min(valid_vals) if valid_vals else 0
        
        # אנחנו יוצרים טווח שמוסיף "אוויר" (padding) בצד ימין (הצד של המספרים הנמוכים כי זה הפוך)
        # הוספתי 15% אוויר בצד ימין (min_val - 15) כדי שהנתונים לא יגעו בשעות (ציר Y)
        safe_max = max_val + 5
        safe_min = min_val - 15

        fig.update_layout(
            margin=dict(l=40, r=20, t=50, b=60), # הורדתי את שולי הימין כי עכשיו ה-range עושה את העבודה
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=max(450, len(labels) * 55), 
            font=dict(family="Assistant"),
            
            legend=dict(
                orientation="h", y=-0.15, x=0.5, xanchor="center", 
                font=dict(size=14, color="#64748b")
            ),
            
            # ציר X קשיח ודינמי שמונע התנגשות טקסט
            xaxis=dict(
                range=[safe_max, safe_min], # החלפנו את ה-autorange בטווח מחושב
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
