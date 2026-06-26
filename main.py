import streamlit as st

def set_rtl():
    st.markdown("""
        <style>
            .stApp, .main, .stSidebar {
                direction: rtl !important;
                text-align: right !important;
            }
            .stSelectbox, .stRadio, .stTextInput, h1, h2, h3, h4, p, li {
                direction: rtl !important;
                text-align: right !important;
            }
            div[data-testid="stHorizontalBlock"] {
                direction: rtl !important;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="פורטל הנתונים - i24NEWS")
set_rtl()

# 3. תוכן דף הבית שלכם
st.markdown("<h1>📺 פורטל הנתונים והמחקר - i24NEWS</h1>", unsafe_allow_html=True)
st.markdown("<p>ברוכים הבאים למערכת הדשבורדים הכללית. בחרו פרויקט מתפריט הצד כדי להתחיל.</p>", unsafe_allow_html=True)
