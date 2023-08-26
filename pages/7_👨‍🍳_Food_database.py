import streamlit as st
import requests
from streamlit_image_select import image_select

st.set_page_config(
    page_title="Food database",
    page_icon="👨‍🍳",
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("# Food database! 👨‍🍳")
st.markdown(
    """
    Add food to your database.
    """
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Add food from openfoodfacts")
with col2:
    st.markdown("### Add food manually")