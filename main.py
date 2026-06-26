import streamlit as st

def set_rtl():
    # כלל CSS אחד קצר שקובע RTL ויישור ימינה לכל אלמנט באפליקציה
    st.markdown("<style>.stApp, .stApp * { direction: rtl !important; text-align: right !important; }</style>", unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="פורטל i24NEWS")
set_rtl()

st.title("📺 פורטל הנתונים והמחקר - i24NEWS")
st.caption("ברוכים הבאים. בחרו פרויקט מתפריט הצד כדי להתחיל.")
