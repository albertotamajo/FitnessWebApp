import pandas as pd
import streamlit as st
import pandas as pd

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

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.expander("""### Food 1"""):
        st.selectbox("Food 1", ["pollo conad conad conad", "aiò maiala"], label_visibility="hidden")
        food1Min = st.number_input('Min', key="food1Min")
        food1Max = st.number_input('Min', key="food1Max")
    with st.expander("""### Food 5"""):
        st.write("hello")
    with st.expander("""### Food 9"""):
        st.write("hello")

with col2:
    with st.expander("""### Food 2"""):
        st.write("hello")
    with st.expander("""### Food 6"""):
        st.write("hello")
    with st.expander("""### Food 10"""):
        st.write("hello")

with col3:
    with st.expander("""### Food 3"""):
        st.write("hello")
    with st.expander("""### Food 7"""):
        st.write("hello")
    with st.expander("""### Food 11"""):
        st.write("hello")

with col4:
    with st.expander("""### Food 4"""):
        st.write("hello")
    with st.expander("""### Food 8"""):
        st.write("hello")
    with st.expander("""### Food 12"""):
        st.write("hello")

data_df = pd.DataFrame(
    {
        "Food": ["hello"],
        "Min": [1],
        "Max":[2]
    }
)

st.data_editor(
    data_df,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        "Food": st.column_config.SelectboxColumn(
            "Food",
            width="large",
            options=[
                "📊 Data Exploration",
                "📈 Data Visualization",
                "🤖 LLM",
            ],
            required=True,
        ),
        "Min" : st.column_config.NumberColumn("Min",width="small", required=True, default=None, format=None,
                                              min_value=0, max_value=1000),
        "Max" : st.column_config.NumberColumn("Max", width="small", required=True, default=None, format=None,
                                              min_value=0, max_value=1000)
    },
    hide_index=True,
)