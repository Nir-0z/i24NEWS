import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import math

st.set_page_config(layout="wide", page_title="השוואת מדרוג ושילוב")

# ==========================================
# 1. מנוע העיצוב (CSS מודולרי, גלובלי, וכוחני)
# ==========================================
st.set_page_config(layout="wide", page_title="השוואת מדרוג ושילוב")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap');
    
    /* פקודת פטיש: כל האתר RTL מימין לשמאל */
    * { font-family: 'Assistant', sans-serif !important; direction: rtl !important; text-align: right !important; }
    
    /* כפיית רקע אפור לעמוד, רקע לבן טהור לכרטיסיות וטקסט שחור */
    .stApp { background-color: #f3f4f6 !important; color: #111827 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
    }
    
    /* פתרון הסטיקי: פריצת מיכל החסימה של סטרימליט ונעילת הכרטיס הראשון */
    [data-testid="stMainBlockContainer"], .main .block-container { overflow: visible !important; }
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type {
        position: sticky !important; top: 3rem !important; z-index: 9999 !important;
    }
    
    /* מודולריות: מחלקות כותרות קבועות ומסודרות */
    .t-main { font-size: 26px; font-weight: 700; color: #111827; margin-bottom: 20px; }
    .t-sec  { font-size: 20px; font-weight: 700; color: #1f2937; margin-bottom: 5px; display: block; }
    .t-q    { font-size: 20px; font-weight: 700; color: #1f2937; margin-bottom: 25px; line-height: 1.4; display: block; }
    
    /* סידור שורת הפילטרים וביטול הקלדה בתיבות הראשונות (העלמת ה-input) */
    [data-testid="stSelectbox"] label { display: none !important; } /* מעלים את הכותרות המובנות של התיבות */
    .filter-label { font-size: 16px; font-weight: 600; padding-top: 10px; margin-left: 10px; }
    
    [data-testid="column"]:nth-of-type(1) [data-baseweb="select"] input,
    [data-testid="column"]:nth-of-type(2) [data-baseweb="select"] input { 
        display: none !important; /* זה הפיצ'ר שמונע הקלדה! */
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. לוגיקת נתונים ופילטרים (קצרה ויעילה)
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "Midrug-Shiluv.csv"))

try: df = load_data()
except Exception: st.error("קובץ הנתונים לא נמצא."); st.stop()

st.markdown("<div class='t-main'>📊 השוואת מדרוג מול סקר שילוב</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("<span class='t-sec'>🎯 סינון נתונים</span>", unsafe_allow_html=True)
    c1, c1b, c2, c2b, c3, c3b = st.columns([0.4, 1.2, 0.4, 1.2, 0.4, 1.5]) # חלוקה מדויקת לכותרות ותיבות
    
    with c1: st.markdown("<div class='filter-label'>ימי מדידה:</div>", unsafe_allow_html=True)
    with c1b: sel_period = st.selectbox("", ["אמצע שבוע", "סוף שבוע"], index=0)
    
    waves = ["גל 19 במאי", "גל 25 במאי", "חיבור שני הגלים"] if sel_period == "אמצע שבוע" else ["גל 17 במאי", "גל 31 במאי", "חיבור שני הגלים"]
    with c2: st.markdown("<div class='filter-label'>גל מחקר:</div>", unsafe_allow_html=True)
    with c2b: sel_wave = st.selectbox("", waves, index=2)
    
    with c3: st.markdown("<div class='filter-label'>פילוח:</div>", unsafe_allow_html=True)
    with c3b:
        if sel_wave == "חיבור שני הגלים":
            df_w = df[(df['period'] == sel_period) & (df['wave'] == sel_wave)]
            opts = df_w.apply(lambda x: "כללי" if x['demo_category'] == "כללי" and x['demo_value'] == "סהכ" else f"{x['demo_category']} - {x['demo_value']}", axis=1).unique()
            sel_demo = st.selectbox("", opts, index=list(opts).index("כללי") if "כללי" in opts else 0)
            cat, val = ("כללי", "סהכ") if sel_demo == "כללי" else sel_demo.split(" - ", 1)
        else:
            st.selectbox("", ["כללי (פילוח בחיבור גלים)"], disabled=True)
            cat, val = "כללי", "סהכ"

df_filtered = df[(df['period'] == sel_period) & (df['wave'] == sel_wave) & (df['demo_category'] == cat) & (df['demo_value'] == val)]

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True) # רווח נשימה

# ==========================================
# 3. מנוע הגרף (פונקציה חכמה אחת במקום בלגן)
# ==========================================
def render_chart(plot_df):
    labels = plot_df['answer_text'].drop_duplicates().tolist()
    if not labels: return st.info("אין נתונים להצגה.")
        
    fig = go.Figure()
    s_vals, m_vals, s_ns = [], [], []
    
    # חילוץ נתונים בלולאה קצרה
    for ans in labels:
        ans_data = plot_df[plot_df['answer_text'] == ans]
        s_row = ans_data[ans_data['source'] == 'שילוב']
        m_row = ans_data[ans_data['source'] == 'מדרוג']
        
        s_vals.append(s_row['percentage'].values[0] if not s_row.empty else None)
        m_vals.append(m_row['percentage'].values[0] if not m_row.empty else None)
        s_ns.append(s_row['n_size'].values[0] if not s_row.empty else None)

    # יצירת הקווים המחברים
    for lbl, s, m in zip(labels, s_vals, m_vals):
        if s is not None and m is not None:
            fig.add_trace(go.Scatter(x=[m, s], y=[lbl, lbl], mode="lines", line=dict(color="#d1d5db", width=2, dash="dot"), showlegend=False))
            
    # פונקציית-עזר חכמה לציור הנקודות והטקסטים למניעת שכפול קוד
    def add_points(vals, name, color, is_left, ns=None):
        texts = [f"<b>{v}%</b>" if v is not None else "" for v in vals]
        hover = []
        for v, n in zip(vals, ns or [None]*len(vals)):
            if v is None: hover.append("")
            else: hover.append(f"<b>{name}:</b> {v}%" + (f"<br><b>N:</b> {int(n)}" if n and not math.isnan(n) else "") + "<extra></extra>")
            
        fig.add_trace(go.Scatter(
            x=vals, y=labels, mode="markers+text", name=name,
            marker=dict(color=color, size=14, line=dict(color='white', width=2)),
            text=texts, textposition="middle left" if is_left else "middle right",
            hovertemplate=hover, textfont=dict(size=14, color=color, family="Assistant")
        ))

    add_points(s_vals, 'סקר שילוב', '#2563eb', True, s_ns)
    add_points(m_vals, 'הוועדה למדרוג', '#ea580c', False)

    # עיצוב מגרש הגרף
    v_all = [v for v in s_vals + m_vals if v is not None]
    mx = max(v_all) if v_all else 100
    
    fig.update_layout(
        margin=dict(l=10, r=200, t=10, b=50),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=max(350, len(labels)*50),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        xaxis=dict(range=[mx*1.15, -(mx*0.3)], showgrid=True, gridcolor="#f3f4f6", zeroline=False, ticksuffix="%"),
        yaxis=dict(side="right", categoryorder="array", categoryarray=labels[::-1], tickfont=dict(size=14, weight="bold", color="#111827"))
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ==========================================
# 4. תצוגת הממשק התחתון
# ==========================================
col_side, col_chart = st.columns([1.3, 2.5], gap="large")

with col_side:
    with st.container(border=True):
        st.markdown("<span class='t-sec'>📋 בחר שאלה לניתוח:</span>", unsafe_allow_html=True)
        questions = df_filtered['question_text'].unique().tolist()
        if not questions: st.warning("אין נתונים."); st.stop()
        sel_q = st.radio("", questions, index=0, label_visibility="collapsed")

with col_chart:
    with st.container(border=True):
        st.markdown(f"<span class='t-q'>📋 {sel_q}</span>", unsafe_allow_html=True)
        render_chart(df_filtered[df_filtered['question_text'] == sel_q])
