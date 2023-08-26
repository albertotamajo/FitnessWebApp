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
st.divider()

cals, carbs, proteins, fats = st.columns(4)

with cals:
   st.markdown("### Calories")
   calsMin = st.number_input('Min', key="calsMin")
   calsMax = st.number_input('Max', key="calsMax")

with carbs:
   st.markdown("### Carbs")
   carbsMin = st.number_input('Min', key="carbsMin")
   carbsMax = st.number_input('Max', key="carbsMax")

with proteins:
   st.markdown("### Proteins")
   prtsMin = st.number_input('Min', key="prtsMin")
   prtsMax = st.number_input('Max', key="prtsMax")

with fats:
   st.markdown("### Fats")
   fatsMin = st.number_input('Min', key="fatsMin")
   fatsMax = st.number_input('Max', key="fatsMax")

st.markdown(
    f"""
    - Calories: min :green[{calsMin}] kcal | max :red[{calsMax}] kcal
    - Carbs: min :green[{carbsMin}] gr | max :red[{carbsMax}] gr
    - Proteins: min :green[{prtsMin}] gr | max :red[{prtsMax}] gr
    - Fats: min :green[{fatsMin}] gr | max :red[{fatsMax}] gr
    """
)

st.divider()

with st.expander("""### Food 1"""):
    pass

with st.expander("""### Food 2"""):
    pass

