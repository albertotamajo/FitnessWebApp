import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from streamlit_image_select import image_select
from st_clickable_images import clickable_images
import concurrent.futures

st.set_page_config(
    page_title="Nutrition analysis",
    page_icon="👨‍🍳",
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)



st.write("# Nutrition analysis! 👨‍🍳")

st.markdown(
    """
    Analyse the nutritional values of your food.
    """
)

query = st.text_input("Write your food here. One food per line.", value="", key="query")
min_g = st.number_input("Select minimum grams", min_value=1, value=50, step=1)
max_g = st.number_input("Select maximum grams", min_value=1, value=50, step=1)
if query != "":
    query = "+".join(query.split())
    url = "https://it.openfoodfacts.org/cgi/search.pl?search_terms={0}&search_simple=1&json=1&action=process"
    search_result = requests.get(url.format(query)).json()
    products = search_result['products'][:10]
    i = image_select("Select food", [p["image_front_small_url"] for p in products if "image_front_small_url" in p],
                                                   return_value="index", use_container_width=False)


