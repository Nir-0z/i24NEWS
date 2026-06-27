import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide", page_title="השוואת מדרוג ושילוב")

# סגנון קבוע בלבד
st.markdown("""
<style>
    * {direction: rtl!important; text-align: right!important;}
    .stRadio > div {padding:1.5rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "Midrug-Shiluv.csv"))

df = load_data()
st.title("📊 השוואת מדרוג מול סקר שילוב")

# אזור הפילטרים
with st.container(border=True):
    cols = st.columns([1.5, 1, 2.5, 1, 2.5, 1.5, 3])
    cols[0].markdown("### 🎯 סינון נתונים")
    cols[1].write("ימי מדידה:")
    sel_p = cols[2].selectbox("", ["אמצע שבוע", "סוף שבוע"], label_visibility="collapsed")
    cols[3].write("גל מחקר:")
    waves = ["גל 19 במאי", "גל 25 במאי", "חיבור שני הגלים"] if sel_p == "אמצע שבוע" else ["גל 17 במאי", "גל 31 במאי", "חיבור שני הגלים"]
    sel_w = cols[4].selectbox("", waves, index=2, label_visibility="collapsed")
    
    cols[5].write("פילוח דמוגרפי:")
    if sel_w == "חיבור שני הגלים":
        opts = df[df['wave'] == "חיבור שני הגלים"].apply(lambda x: "כללי" if x['demo_category'] == "כללי" else f"{x['demo_category']} - {x['demo_value']}", axis=1).unique()
        sel_d = cols[6].selectbox("", opts, index=list(opts).index("כללי") if "כללי" in opts else 0, label_visibility="collapsed")
        cat, val = ("כללי", "סהכ") if sel_d == "כללי" else sel_d.split(" - ", 1)
    else:
        cols[6].selectbox("", ["כללי (זמין בחיבור הגלים)"], disabled=True, label_visibility="collapsed")
        cat, val = "כללי", "סהכ"

df_f = df[(df['period'] == sel_p) & (df['wave'] == sel_w) & (df['demo_category'] == cat) & (df['demo_value'] == val)]
st.divider()

# אזור התצוגה - תפריט לצד גרף
q_list = df_f['question_text'].unique().tolist()
if not q_list: 
    st.warning("אין נתונים עבור הסינון שנבחר.")
    st.stop()

menu_col, chart_col = st.columns([1.3, 2.5], gap="large")

with menu_col:
    with st.container(border=True):
        st.markdown("### 📋 בחר שאלה לניתוח:")
        sel_q = st.radio("", q_list, label_visibility="collapsed")

plot_df = df_f[df_f['question_text'] == sel_q]
labels = plot_df['answer_text'].drop_duplicates().tolist()

with chart_col:
    with st.container(border=True):
        if labels:
            fig = go.Figure()
            s_vals, m_vals = [], []
            
            for ans in labels:
                s_row = plot_df[(plot_df['answer_text'] == ans) & (plot_df['source'] == 'שילוב')]
                m_row = plot_df[(plot_df['answer_text'] == ans) & (plot_df['source'] == 'מדרוג')]
                
                s_v = s_row['percentage'].values[0] if not s_row.empty else None
                m_v = m_row['percentage'].values[0] if not m_row.empty else None
                s_vals.append(s_v)
                m_vals.append(m_v)

                if s_v is not None and m_v is not None:
                    fig.add_trace(go.Scatter(
                        x=[m_v, s_v], y=[ans, ans], mode="lines", 
                        line=dict(color="#d1d5db", width=2, dash="dot"), showlegend=False
                    ))
                    
            def add_points(vals, source_name, color, is_left):
                # טקסט מוצמד תמיד: מימין לערך הנמוך, משמאל לערך הגבוה
                texts = []
                text_positions = []
                for v in vals:
                    texts.append(f"<b>{v}%</b>" if v is not None else "")
                
                for v, m in zip(vals, m_vals):
                    if v is None:
                        text_positions.append("middle right")
                    elif is_left: # סקר שילוב
                        text_positions.append("middle left")
                    else: # מדרוג
                        text_positions.append("middle right")

                hover_texts = [
                    f"<b>{source_name}</b><br>אחוז: {v}%<extra></extra>" if v is not None else "" 
                    for v in vals
                ]
                
                fig.add_trace(go.Scatter(
                    x=vals, y=labels, mode="markers+text", name=source_name,
                    marker=dict(color=color, size=14, line=dict(color='white', width=2)),
                    text=texts, textfont=dict(size=13, color=color),
                    textposition=text_positions,
                    hovertemplate=hover_texts
                ))

            # שילוב מופיע ראשון (נקודה שמאלית/ימנית בהתאם לערך) ומדרוג שני
            add_points(s_vals, 'סקר שילוב', '#2563eb', True)
            add_points(m_vals, 'הוועדה למדרוג', '#ea580c', False)

            v_all = [v for v in s_vals + m_vals if v is not None]
            mx = max(v_all, default=100)
            
            fig.update_layout(
                # הגדלת ה-margin הימני כדי למנוע חיתוך של תוויות התשובות הארוכות
                margin=dict(l=10, r=100, t=20, b=60), 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=max(350, len(labels)*60),
                # הזזה ומרווח למקרא כדי שלא יפריע ללייבלים
                legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
                xaxis=dict(
                    range=[mx*1.15, -(mx*0.3)], showgrid=True, gridcolor="#f3f4f6", 
                    zeroline=False, ticksuffix="%"
                ),
                yaxis=dict(
                    side="right", categoryorder="array", categoryarray=labels[::-1], 
                    tickfont=dict(size=14, weight="bold")
                )
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("אין נתונים להצגת תרשים עבור שאלה זו.")
