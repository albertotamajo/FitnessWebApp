import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from streamlit_image_select import image_select
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


def fetch_image(product, id):
    image = Image.new("RGB", (28, 28))
    if "image_front_small_url" in product.keys():
        response = requests.get(product["image_front_small_url"])
        image = Image.open(BytesIO(response.content))
    return id, image


st.write("# Nutrition analysis! 👨‍🍳")

st.markdown(
    """
    Analyse the nutritional values of your food.
    """
)

query = st.text_input("Write your food here. One food per line.", value="")
count = st.number_input('Number of items searched', min_value=1, max_value=100, value=5, step=1)
if st.button('Find food'):
    if query == "":
        st.error('You need to write some food')
    else:
        query = "+".join(query.split())
        url = "https://it.openfoodfacts.org/cgi/search.pl?search_terms={0}&search_simple=1&json=1&action=process"
        search_result = requests.get(url.format(query)).json()
        products = search_result['products'][:count]
        print(len(products))
        images = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(products)) as executor:
            future_to_url = (executor.submit(fetch_image, p, i) for i, p in enumerate(products))
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    images.append(data)
        images.sort()
        images = [img for id, img in images]
        index = image_select("Select food", images, return_value="index", use_container_width=False)

