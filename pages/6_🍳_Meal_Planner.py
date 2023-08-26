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

cals, carbs, proteins, fats = st.columns(4)

with cals:
   st.header("Calories")
   calsMin = st.number_input('Min', key="calsMin")
   calsMax = st.number_input('Max', key="calsMax")

with carbs:
   st.header("Carbs")
   carbsMin = st.number_input('Min', key="carbsMin")
   carbsMax = st.number_input('Max', key="carbsMax")

with proteins:
   st.header("Proteins")
   prtsMin = st.number_input('Min', key="prtsMin")
   prtsMax = st.number_input('Max', key="prtsMax")

with fats:
   st.header("Fats")
   fatsMin = st.number_input('Min', key="fatsMin")
   fatsMax = st.number_input('Max', key="fatsMax")

st.markdown(
    f"""
    - Calories: min :green[calsMin] kcal | max :red[calsMax] kcal
    - Carbs: min :green[carbsMin] gr | max :red[carbsMax] gr
    - Proteins: min :green[prtsMin] gr | max :red[prtsMax] gr
    - Fats: min :green[fatsMin] gr | max :red[fatsMax] gr
    """
)