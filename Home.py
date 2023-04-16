import streamlit as st

AWS_BUCKET="fitnessmanagement/"

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to the Fitness Management Web App! 👋")

st.sidebar.success("Select one of these functionalities.")

st.markdown(
    """
    This web app is used by Alberto Tamajo and Giuseppe Mistretta.
"""
)