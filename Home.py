import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

AWS_BUCKET="fitnessmanagement/"


st.write("# Welcome to the Fitness Management Web App! 👋")

st.sidebar.success("Select one of these functionalities.")

st.markdown(
    """
    This web app is used by Alberto Tamajo and Giuseppe Mistretta.
"""
)