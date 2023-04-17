import streamlit as st
import pickle
import pytz
import s3fs
from datetime import datetime

st.set_page_config(
    page_title="Visualise statistics",
    page_icon="📈",
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

AWS_BUCKET="fitnessmanagement/"

fs = s3fs.S3FileSystem(anon=False)
print(fs.ls("fitnessmanagement/"))


st.write("# Visualise statistics! 📈")

EXERCISE_LIST_PATH = "exercises.txt"
with open(EXERCISE_LIST_PATH, 'rb') as f:
    exercise_list = [str(e, 'utf-8') for e in f.readlines()]
    exercise_list.sort()
    exercise_list = ['<select>'] + exercise_list

st.markdown(
    """
    Visualise the statistics about one or more exercises.
    """
)
