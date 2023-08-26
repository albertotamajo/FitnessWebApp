import streamlit as st
import s3fs
import requests

@st.cache_resource
def s3fs_file_system():
    return s3fs.S3FileSystem(anon=False)

url = "https://it.openfoodfacts.org/cgi/search.pl?search_terms=muesli+conad&search_simple=1&json=1&action=process"
search_result = requests.get(url.format(url)).json()
products = search_result['products'][:10]
products

