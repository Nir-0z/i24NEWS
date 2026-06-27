st.markdown("""
<style>
    * {direction: rtl!important; text-align: right!important;}
    
    /* מרווח וקו תחתון בין אפשרויות הרדיו וריווח הלייבל מהאפשרויות */
    .stRadio label {
        padding: 15px 0 !important;
        border-bottom: 1px solid #f3f4f6;
    }
    
    /* הרחקת כותרת/נוסח השאלה מכפתור הבחירה הראשון ברשימה */
    div.row-widget.stRadio > div > label:first-of-type {
        margin-bottom: 10px;
    }
    
    /* דריסת כיווניות עבור אזור התרשים בלבד */
    div[data-testid="stPlotlyChart"] * {
        direction: ltr !important;
        text-align: left !important;
        unicode-bidi: isolate !important;
    }
    div[data-testid="stPlotlyChart"] {
        direction: ltr !important;
        text-align: left !important;
    }
</style>
""", unsafe_allow_html=True)
