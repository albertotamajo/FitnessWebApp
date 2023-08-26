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
   calsMax = st.number_input('Max', key="calsMax")
   calsMin = st.number_input('Min', key="calsMin")

with carbs:
   st.markdown("### Carbs")
   carbsMax = st.number_input('Max', key="carbsMax")
   carbsMin = st.number_input('Min', key="carbsMin")

with proteins:
   st.markdown("### Proteins")
   prtsMax = st.number_input('Max', key="prtsMax")
   prtsMin = st.number_input('Min', key="prtsMin")

with fats:
   st.markdown("### Fats")
   fatsMax = st.number_input('Max', key="fatsMax")
   fatsMin = st.number_input('Min', key="fatsMin")

st.markdown(
    f"""
    - Calories: min :green[{calsMin}] kcal | max :red[{calsMax}] kcal
    - Carbs: min :green[{carbsMin}] gr | max :red[{carbsMax}] gr
    - Proteins: min :green[{prtsMin}] gr | max :red[{prtsMax}] gr
    - Fats: min :green[{fatsMin}] gr | max :red[{fatsMax}] gr
    """
)

st.divider()

# col1, col2, col3, col4 = st.columns(4)
#
# with col1:
#     with st.expander("""### Food 1"""):
#         st.selectbox("Food 1", ["pollo conad conad conad", "aiò maiala"], label_visibility="hidden")
#         food1Min = st.number_input('Min', key="food1Min")
#         food1Max = st.number_input('Min', key="food1Max")
#     with st.expander("""### Food 5"""):
#         st.write("hello")
#     with st.expander("""### Food 9"""):
#         st.write("hello")
#
# with col2:
#     with st.expander("""### Food 2"""):
#         st.write("hello")
#     with st.expander("""### Food 6"""):
#         st.write("hello")
#     with st.expander("""### Food 10"""):
#         st.write("hello")
#
# with col3:
#     with st.expander("""### Food 3"""):
#         st.write("hello")
#     with st.expander("""### Food 7"""):
#         st.write("hello")
#     with st.expander("""### Food 11"""):
#         st.write("hello")
#
# with col4:
#     with st.expander("""### Food 4"""):
#         st.write("hello")
#     with st.expander("""### Food 8"""):
#         st.write("hello")
#     with st.expander("""### Food 12"""):
#         st.write("hello")


convert_dict = {'Food': str,
                'Min(gr)': int,
                'Max(gr)': int
                }
data_df = pd.DataFrame(
    {
        "Food": [],
        "Min(gr)": [],
        "Max(gr)":[]
    }
).astype(convert_dict)


food_table = st.data_editor(
    data_df,
    use_container_width=False,
    num_rows="dynamic",
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
        "Min(gr)":st.column_config.NumberColumn("Min(gr)", width="small", required=True, default=0, format=None,
                                              min_value=0, max_value=1000),
        "Max(gr)":st.column_config.NumberColumn("Max(gr)", width="small", required=True, default=0, format=None,
                                              min_value=0, max_value=1000)
    },
    hide_index=True,
)

print(food_table)

