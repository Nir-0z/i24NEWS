import streamlit as st

def set_rtl():
    st.markdown("""
        <style>
            /* רקע אפרפר מודרני לכל האתר */
            .stApp { 
                background-color: #f8fafc !important; 
            }
            
            /* שדרוג הכרטיסים המובנים של סטרימליט למראה יוקרתי */
            div[data-testid="stVerticalBlockBorder"] {
                background-color: #ffffff !important;
                padding: 24px !important;
                border-radius: 16px !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
                border: 1px solid #e2e8f0 !important;
                margin-bottom: 20px !important;
            }

            /* RTL ויישור ימינה מושלם לכל אלמנט */
            .stApp, .stApp * { 
                direction: rtl !important; 
                text-align: right !important; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            }
            
            /* תיקון יישור ספציפי לכפתורי הרדיו של השאלות */
            div[data-testid="stRadio"] label {
                justify-content: flex-start !important;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="פורטל i24NEWS")
set_rtl()

st.markdown("<h1 style='color: #1e293b; margin-bottom: 10px;'>📺 פורטל הנתונים והמחקר - i24NEWS</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b;'>ברוכים הבאים למערכת הדשבורדים החדשה.</p>", unsafe_allow_html=True)
