import streamlit as st

pg = st.navigation([st.Page("pages/report_generation.py", title="Report Generation"),st.Page("pages/chat.py", title="Start Chat")])
pg.run()