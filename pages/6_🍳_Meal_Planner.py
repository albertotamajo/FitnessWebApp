import streamlit as st
import requests

st.set_page_config(
    page_title="Meal planner",
    page_icon="🍳",
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("# Meal planner! 🍳")
st.markdown(
    """
    Set your meal objectives, select your food and let me compute the quantity of food you need.
    """
)

cals, carbs, proteins, fats = st.columns(3)

with cals:
   st.header("Calories")
   st.number_input('Min')
   st.number_input('Max')
with carbs:
   st.header("Carbohydrates")
   st.number_input('Min')
   st.number_input('Max')

with proteins:
   st.header("Proteins")
   st.number_input('Min')
   st.number_input('Max')

with fats:
   st.header("Fats")
   st.number_input('Min')
   st.number_input('Max')