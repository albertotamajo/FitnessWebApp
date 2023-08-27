import pandas as pd
import streamlit as st
import pandas as pd
import utils
import pickle
from pulp import *
st.set_page_config(
    page_title="Meal",
    page_icon="🍳",
)

AWS_BUCKET = "fitnessmanagement/"
file = "{0}Food.pickle".format(AWS_BUCKET)
fs = utils.s3fs_file_system()
fs.clear_instance_cache()

#@st.cache_data
def fetch_food():
    # Fetch data from URL here, and then clean it up.
    if fs.exists(file):
        with fs.open(file, 'rb') as f:
            d = pickle.load(f)
        return d
    else:
        return {}

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("# Meal! 🍳")

with st.expander("Plan your meal"):
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

    food_dict = fetch_food()

    food_table = st.data_editor(
        data_df,
        use_container_width=False,
        num_rows="dynamic",
        column_config={
            "Food": st.column_config.SelectboxColumn(
                "Food",
                width="large",
                options=list(food_dict.keys()),
                required=True,
            ),
            "Min(gr)":st.column_config.NumberColumn("Min(gr)", width="small", required=True, default=0, format=None,
                                                  min_value=0, max_value=1000),
            "Max(gr)":st.column_config.NumberColumn("Max(gr)", width="small", required=True, default=0, format=None,
                                                  min_value=0, max_value=1000)
        },
        hide_index=True,
    )

    if st.button("Compute meal plan"):
        # Instantiate model
        model = LpProblem("MealPlan", LpMaximize)
        # Instantiate decision variables
        decision_variables = [LpVariable(name=food_table["Food"][ind], lowBound=food_table["Min(gr)"][ind],
                                         upBound=food_table["Max(gr)"][ind], cat=LpInteger) for ind in food_table.index]
        # Add Objective function
        model += lpSum(decision_variables)

        # Add constraints
        model += lpSum([decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in food_table.index])\
                 >= calsMin, "minCalories"
        model += lpSum([decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in food_table.index])\
                 <= calsMax, "maxCalories"
        model += lpSum([decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in food_table.index]) \
                 >= carbsMin, "minCarbs"
        model += lpSum([decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in food_table.index]) \
                 <= carbsMax, "maxCarbs"
        model += lpSum([decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in food_table.index]) \
                 >= prtsMin, "minProteins"
        model += lpSum([decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in food_table.index]) \
                 <= prtsMax, "maxProteins"
        model += lpSum([decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in food_table.index]) \
                 >= fatsMin, "minFats"
        model += lpSum([decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in food_table.index]) \
                 <= fatsMax, "maxFats"

        # The problem is solved using PuLP's Solver
        status = LpStatus[model.solve()]
        st.divider()
        if status is "Optimal":
            dict = {"Food": [v.name.replace("_", " ") for v in model.variables()],
                    "Qnt(gr)": [v.varValue for v in model.variables()],
                    "Cals(kcal)": [food_dict[v.name.replace("_", " ")]["Cals"] * v.varValue for v in model.variables()],
                    "Carbs(gr)": [food_dict[v.name.replace("_", " ")]["Carbs"] * v.varValue for v in model.variables()],
                    "Proteins(gr)": [food_dict[v.name.replace("_", " ")]["Proteins"] * v.varValue for v in model.variables()],
                    "Fats(gr)": [food_dict[v.name.replace("_", " ")]["Fats"] * v.varValue for v in model.variables()]}
            df = pd.DataFrame(dict)
            df.loc['Total'] = df.sum(numeric_only=True)
            st.dataframe(df)
            df.to_excel("my_meal_plan.xlsx")
            with open("my_meal_plan.xlsx", "rb") as f:
                st.download_button("Download meal plan", f, file_name="my_meal_plan.xlsx")

        else:
            st.error(f"Solver error: status {status}")

with st.expander("Compute meal's nutritional values"):

    convert_dict = {'Food': str,
                    'Qnt(gr)': int
                    }
    data_df = pd.DataFrame(
        {
            "Food": [],
            "Qnt(gr)": []
        }
    ).astype(convert_dict)

    food_dict = fetch_food()

    food_table = st.data_editor(
        data_df,
        use_container_width=False,
        num_rows="dynamic",
        column_config={
            "Food": st.column_config.SelectboxColumn(
                "Food",
                width="large",
                options=list(food_dict.keys()),
                required=True,
            ),
            "Qnt(gr)": st.column_config.NumberColumn("Qnt(gr)", width="small", required=True, default=0, format=None,
                                                     min_value=0, max_value=1000)
        },
        hide_index=True,
    )
    if st.button("Compute nutritional values"):
        dict = {
            "Food": [food_table["Food"][ind] for ind in food_table.index],
            "Qnt(gr)": [food_table["Qnt(gr)"][ind] for ind in food_table.index],
            "Cals(kcal)": [food_dict[food_table["Food"][ind]]["Cals"] * food_table["Qnt(gr)"][ind] for ind in food_table.index],
            "Carbs(gr)": [food_dict[food_table["Food"][ind]]["Carbs"] * food_table["Qnt(gr)"][ind] for ind in food_table.index],
            "Proteins(gr)": [food_dict[food_table["Food"][ind]]["Proteins"] * food_table["Qnt(gr)"][ind] for ind in food_table.index],
            "Fats(gr)": [food_dict[food_table["Food"][ind]]["Fats"] * food_table["Qnt(gr)"][ind] for ind in food_table.index]
        }
        df = pd.DataFrame(dict)
        df.loc['Total'] = df.sum(numeric_only=True)
        st.dataframe(df)
        df.to_excel("my_meal_nutrition.xlsx")
        with open("my_meal_nutrition.xlsx", "rb") as f:
            st.download_button("Download meal nutrition", f, file_name="my_meal_nutrition.xlsx")
