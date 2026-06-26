import streamlit as st

def set_rtl():
    # ה-CSS היוקרתי מוזרק ישירות כטקסט קבוע כדי למנוע בעיות קריאת קבצים
    css_content = """
        <style>
            /* 1. רקע עמוק ואקסקלוסיבי לכל המערכת */
            .stApp { 
                background-color: #f1f5f9 !important; 
            }
            
            /* 2. כרטיסי פרימיום לבנים - פדינג ענק (45px) לעיצוב נשימה ומרווח */
            div[data-testid="stVerticalBlockBorder"] {
                background-color: #ffffff !important;
                padding: 35px 40px !important;
                border-radius: 24px !important;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05) !important;
                border: none !important;
                margin-bottom: 25px !important;
            }

            /* 3. שליטה מוחלטת ב-RTL ויישור ימינה של המערכת */
            .stApp, .stApp * { 
                direction: rtl !important; 
                text-align: right !important; 
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif !important;
            }
            
            /* 4. תיקון קשיח ליישור התיבות הנפתחות (Dropdowns) מימין לשמאל */
            div[data-baseweb="select"] *, div[data-testid="stSelectbox"] * {
                text-align: right !important;
                direction: rtl !important;
            }
            div[data-testid="stSelectbox"] div {
                direction: rtl !important;
                text-align: right !important;
            }
            
            /* 5. סידור כפתורי הרדיו של השאלות שלא ימחצו ויהיו מרווחים */
            div[data-testid="stRadio"] label {
                justify-content: flex-start !important;
                padding: 8px 0 !important;
            }
        </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)

# הגדרות עמוד הבית הראשי
st.set_page_config(layout="wide", page_title="פורטל i24NEWS")
set_rtl()

st.markdown("<h1 style='color: #0f172a; font-weight: 700; margin-bottom: 10px;'>📺 פורטל הנתונים והמחקר - i24NEWS</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #475569;'>ברוכים הבאים. בחרו פרויקט מתפריט הצד כדי להתחיל.</p>", unsafe_allow_html=True)
