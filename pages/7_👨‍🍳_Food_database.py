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


with st.expander("""### Add food from openfoodfacts"""):
    query = st.text_input("Write the name of the food", value="")
    query = "+".join(query.split())
    url = "https://it.openfoodfacts.org/cgi/search.pl?search_terms={0}&search_simple=1&json=1&action=process"
    search_result = requests.get(url.format(query)).json()

with st.expander("""### Add food manually"""):
    food_name = st.text_input("Write the name of the food", value="")
    calories = st.number_input('Write the calories of this food (100gr)', min_value=int(0), max_value=int(1000), step=1)
    carbs = st.number_input('Write the carbs of this food (100gr)', min_value=int(0), max_value=int(1000), step=1)
    proteins = st.number_input('Write the proteins of this food (100gr)', min_value=int(0), max_value=int(1000), step=1)
    fats = st.number_input('Write the fats of this food (100gr)', min_value=int(0), max_value=int(1000), step=1)