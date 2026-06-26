import streamlit as st

def set_rtl():
    st.markdown("""
        <style>
            /* רקע כללי בהיר ואפרפר לכל האתר */
            .stApp { 
                background-color: #f8fafc !important; 
            }
            
            /* עיצוב כרטיס לבן, יוקרתי ומרווח */
            .custom-card {
                background-color: #ffffff !important;
                padding: 24px !important;
                border-radius: 16px !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
                margin-bottom: 24px !important;
                border: 1px solid #f1f5f9 !important;
            }

            /* יישור גורף לימין וכיוון RTL */
            .stApp, .stApp * { 
                direction: rtl !important; 
                text-align: right !important; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            }

            /* ניקוי שוליים מיותרים של סטרימליט בתוך הטורים */
            div[data-testid="stBlock"] {
                margin-bottom: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)

# הגדרות דף הבית הראשי
st.set_page_config(layout="wide", page_title="פורטל i24NEWS")
set_rtl()

st.markdown("<h1 style='color: #1e293b; margin-bottom: 10px;'>📺 פורטל הנתונים והמחקר - i24NEWS</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b;'>ברוכים הבאים. בחרו פרויקט מתפריט הצד או מהקישורים כדי להתחיל.</p>", unsafe_allow_html=True)
