import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import openfoodfacts
from streamlit_image_select import image_select

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

query = st.text_input("Write your food here. One food per line.", value="")
count = st.number_input('Number of items searched', min_value=1, max_value=100, value=5, step=1)
password = st.text_input('Password')
if st.button('Find food'):
    if password != st.secrets["PASSWORD"] or query == "":
        if password != st.secrets["PASSWORD"]:
            st.error('You need to type a correct password')
        if query != "":
            st.error('You need to write some food')
    else:
        search_result = openfoodfacts.products.search(query, page_size=count, locale="it")
        products = search_result['products']
        print("Done1")
        images = []
        urls = []
        for p in products:
            if "image_front_url" in p.keys():
                response = requests.get(p["image_front_url"])
                images.append(Image.open(BytesIO(response.content)))
            else:
                images.append(Image.new("RGB", (28, 28)))
        print("Done")
        index = image_select("Select food", images, return_value="index", use_container_width=False)

