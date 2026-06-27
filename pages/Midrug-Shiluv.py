import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. הגדרת עמוד והזרקת RTL ועיצוב פרימיום
st.set_page_config(layout="wide", page_title="השוואת מדרוג ושילוב")

st.markdown("""
    <style>
        /* ייבוא פונט פרימיום מגוגל */
        @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;800&display=swap');
        
        /* החלת הפונט וכיווניות על כל האפליקציה */
        .stApp, .stApp * {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Assistant', sans-serif !important;
        }
        
        /* רקע כללי - אפור סופר-בהיר ויוקרתי */
        .stApp {
            background-color: #f4f7f9 !important;
        }
        
        /* כרטיסיות פרימיום - הצללה רב-שכבתית וגבולות עדינים */
        div[data-testid="stBlock"], div[data-testid="stVerticalBlockBorder"] {
            background: #ffffff !important;
            padding: 35px 40px !important;
            border-radius: 24px !important;
            box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0,0,0,0.03) !important;
            border: 1px solid rgba(226, 232, 240, 0.6) !important;
            margin-bottom: 30px !important;
            transition: all 0.3s ease;
        }
        
        /* שדרוג כותרות - טקסט בגרדיאנט */
        h2 {
            background: linear-gradient(90deg, #0f172a 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
            margin-bottom: 25px !important;
        }
        
        /* עיצוב הפילטרים - מראה עגול ונקי יותר */
        div[data-baseweb="select"] > div {
            border-radius: 12px !important;
            border: 1px solid #e2e8f0 !important;
            background-color: #f8fafc !important;
        }
        
        div[data-baseweb="select"] *, div[data-testid="stSelectbox"] *, .stSelectbox div {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* כפתורי רדיו אלגנטיים */
        div[data-testid="stRadio"] label {
            direction: rtl !important;
            text-align: right !important;
            justify-content: flex-start !important;
            padding: 10px 12px !important;
            border-radius: 8px;
            transition: background 0.2s ease;
        }
        div[data-testid="stRadio"] label:hover {
            background-color: #f1f5f9 !important;
        }
        
        /* כותרות הפילטרים והווידג'טים */
        div[data-testid="stWidgetLabel"] p {
            font-weight: 600 !important;
            color: #475569 !important;
            margin-bottom: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. טעינת הנתונים מהאקסל בבטחה
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
    st.error("לא נמצאו שאלות תקינות בקובץ (המתחילות ב-'q' או מכילות ':'). אנא בדוק את מבנה האקסל.")
    st.stop()

# בניית פילוח דמוגרפי דינמי
cats = [str(x).strip() if pd.notna(x) else "" for x in df_s.iloc[0]]
for i in range(1, len(cats)): 
    if not cats[i]: cats[i] = cats[i-1]

demo = {"כללי": 3}
for idx in range(4, df_s.shape[1]):
    sub = df_s.iloc[1, idx]
    if pd.notna(sub): demo[f"{cats[idx]} - {str(sub).strip()}"] = idx

# 3. כותרת עליונה
st.markdown("<h2>📊 השוואת מדרוג מול סקר שילוב</h2>", unsafe_allow_html=True)

# 4. אזור פילטרים עליון
col_f1, col_f2, _, _ = st.columns([1.5, 1.5, 1, 1])
with col_f1:
    wave = st.selectbox("גל מחקר:", ["חיבור שניהם", "גל 19 במאי", "גל 25 במאי"])
with col_f2:
    if wave == "חיבור שניהם":
        t_col = demo.get(st.selectbox("פילוח דמוגרפי:", list(demo.keys())), 3)
    else:
        t_col = 1 if wave == "גל 19 במאי" else 2

# 5. חלוקת המבנה לטורים
col_side, col_chart = st.columns([1, 2.2], gap="large")

with col_side:
    st.markdown("<p style='font-weight: 600; color: #475569; margin-bottom: 10px;'>בחר שאלה לניתוח:</p>", unsafe_allow_html=True)
    sel_q = st.radio("", list(questions.keys()), label_visibility="collapsed")

with col_chart:
    labels, s_vals, m_vals = [], [], []
    start_row = questions[sel_q] + 1
    
    # חילוץ וניקוי נתונים
    for i in range(start_row, len(df_s)):
        row_s = df_s.iloc[i]
        if pd.isna(row_s[0]) or "q" in str(row_s[0]).lower(): 
            break
            
        txt = str(row_s[0]).lower().replace(" ", "")
        if any(x in txt for x in ["total", "סהכ", "מדגם"]): 
            continue
        
        # הבטחת חילוץ בטוח ללא קריסות אינדקס
        s_val_raw = row_s[t_col] if t_col < len(row_s) else None
        m_val_raw = df_m.iloc[i, t_col] if i < len(df_m) and t_col < len(df_m.iloc[i]) else None
        
        s_val = pd.to_numeric(s_val_raw, errors='coerce')
        m_val = pd.to_numeric(m_val_raw, errors='coerce')
        
        labels.append(str(row_s[0]))
        s_vals.append(float(s_val) if pd.notna(s_val) else None)
        m_vals.append(float(m_val) if pd.notna(m_val) else None)

    if not labels or (all(x is None for x in s_vals) and all(x is None for x in m_vals)):
        st.info("לא נמצאו נתונים כמותיים להצגה עבור שאלה זו בפילוח שנבחר.")
    else:
        fig = go.Figure()
        
        # קווי רקע מחברים עדינים (מקווקוים למראה נקי)
        for lbl, s_v, m_v in zip(labels, s_vals, m_vals):
            if s_v is not None and m_v is not None:
                fig.add_trace(go.Scatter(
                    x=[m_v, s_v], y=[lbl, lbl], mode="lines", 
                    line=dict(color="#cbd5e1", width=2, dash="dot"), hoverinfo="skip", showlegend=False
                ))

        # נקודות סקר שילוב (כחול פרימיום)
        fig.add_trace(go.Scatter(
            x=s_vals, y=labels, mode="markers+text", name='סקר שילוב', 
            marker=dict(color='#3b82f6', size=14, line=dict(color='white', width=3)),
            text=[f"<b>{x:.1f}%</b>" if x is not None else "" for x in s_vals], 
            textfont=dict(size=13, color="#2563eb", family="Assistant"), 
            textposition="top center",
            hovertemplate="<b>סקר שילוב:</b> %{x}%<extra></extra>"
        ))
        
        # נקודות הוועדה למדרוג (כתום אלגנטי)
        fig.add_trace(go.Scatter(
            x=m_vals, y=labels, mode="markers+text", name='הוועדה למדרוג', 
            marker=dict(color='#f97316', size=14, line=dict(color='white', width=3)),
            text=[f"<b>{x:.1f}%</b>" if x is not None else "" for x in m_vals], 
            textfont=dict(size=13, color="#ea580c", family="Assistant"), 
            textposition="bottom center",
            hovertemplate="<b>מדרוג:</b> %{x}%<extra></extra>"
        ))

        # פריסה יציבה ואלגנטית (ללא שגיאות pad)
        fig.update_layout(
            margin=dict(l=40, r=220, t=50, b=60), 
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=max(400, len(labels) * 55), 
            font=dict(family="Assistant"),
            
            legend=dict(
                orientation="h", y=-0.15, x=0.5, xanchor="center", 
                font=dict(size=14, color="#64748b"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="#e2e8f0",
                borderwidth=1
            ),
            
            # היפוך ציר בטוח (מאפשר לגרף לנשום ללא קיבוע קשיח ל-100)
            xaxis=dict(
                autorange="reversed", 
                showgrid=True, 
                gridcolor="#f1f5f9", 
                gridwidth=1,
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
