import streamlit as st

def set_rtl():
    st.markdown("""
        <style>
            /* רקע אפור-עמוק יוקרתי לאתר */
            .stApp { 
                background-color: #f1f5f9 !important; 
            }
            
            /* עיצוב כרטיסים לבנים בולטים עם צל עמוק וריווח */
            div[data-testid="stVerticalBlockBorder"] {
                background-color: #ffffff !important;
                padding: 30px !important;
                border-radius: 16px !important;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05) !important;
                border: none !important;
                margin-bottom: 24px !important;
            }

            /* הגדרת RTL ויישור גורף */
            .stApp, .stApp * { 
                direction: rtl !important; 
                text-align: right !important; 
                font-family: 'Segoe UI', system-ui, sans-serif !important;
            }
            
            /* יישור ימינה קפדני לתוכן של ה-Dropdowns */
            div[data-baseweb="select"] * {
                text-align: right !important;
                direction: rtl !important;
            }
            div[data-testid="stSelectbox"] label {
                text-align: right !important;
                width: 100%;
            }
            
            /* סידור רשימת הרדיו של השאלות שלא תימחץ */
            div[data-testid="stRadio"] label {
                justify-content: flex-start !important;
                padding: 4px 0;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="פורטל i24NEWS")
set_rtl()
