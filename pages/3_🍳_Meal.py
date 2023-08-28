import pandas as pd
import streamlit as st
import pandas as pd
import utils
import pickle
from pulp import *
import streamlit_authenticator as stauth
import yaml
import numpy as np
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Meal",
    page_icon="🍳",
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    AWS_BUCKET = "fitnessmanagement/"
    file = "{0}Food.pickle".format(AWS_BUCKET)
    fs = utils.s3fs_file_system()
    fs.clear_instance_cache()


    # @st.cache_data
    def fetch_food():
        # Fetch data from URL here, and then clean it up.
        if fs.exists(file):
            with fs.open(file, 'rb') as f:
                d = pickle.load(f)
            return d
        else:
            return {}


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
                "Max(gr)": []
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
                "Min(gr)": st.column_config.NumberColumn("Min(gr)", width="small", required=True, default=0,
                                                         format=None,
                                                         min_value=0, max_value=1000),
                "Max(gr)": st.column_config.NumberColumn("Max(gr)", width="small", required=True, default=0,
                                                         format=None,
                                                         min_value=0, max_value=1000)
            },
            hide_index=True,
        )
        st.divider()
        st.markdown("## Optimisation choices")
        calsOpt, carbsOpt, proteinsOpt, fatsOpt = st.columns(4)
        options = ["None", "Maximise", "Minimise"]
        with calsOpt:
            st.markdown("### Calories")
            calsDec = st.selectbox("", options=options, key="calsDec")

        with carbsOpt:
            st.markdown("### Carbs")
            carbsDec = st.selectbox("", options=options, key="carbsDec")

        with proteinsOpt:
            st.markdown("### Proteins")
            proteinsDec = st.selectbox("", options=options, key="proteinsDec")

        with fatsOpt:
            st.markdown("### Fats")
            fatsDec = st.selectbox("", options=options, key="fatsDec")

        st.divider()
        if st.button("Compute meal plan"):
            optim = LpMaximize
            # Instantiate model
            model = LpProblem("MealPlan", optim)
            # Instantiate decision variables
            decision_variables = [LpVariable(name=food_table["Food"][ind], lowBound=food_table["Min(gr)"][ind],
                                             upBound=food_table["Max(gr)"][ind], cat=LpInteger) for ind in
                                  food_table.index]
            # Add Objective function
            model += lpSum(decision_variables)

            # Add constraints
            model += lpSum(
                [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in food_table.index]) \
                     >= calsMin, "minCalories"
            model += lpSum(
                [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in food_table.index]) \
                     <= calsMax, "maxCalories"
            model += lpSum(
                [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in food_table.index]) \
                     >= carbsMin, "minCarbs"
            model += lpSum(
                [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in food_table.index]) \
                     <= carbsMax, "maxCarbs"
            model += lpSum(
                [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in food_table.index]) \
                     >= prtsMin, "minProteins"
            model += lpSum(
                [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in food_table.index]) \
                     <= prtsMax, "maxProteins"
            model += lpSum(
                [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in food_table.index]) \
                     >= fatsMin, "minFats"
            model += lpSum(
                [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in food_table.index]) \
                     <= fatsMax, "maxFats"

            # The problem is solved using PuLP's Solver
            status = LpStatus[model.solve()]
            st.divider()
            if status is "Optimal":
                dict = {"Food": [v.name.replace("_", " ") for v in model.variables()],
                        "Qnt(gr)": [v.varValue for v in model.variables()],
                        "Cals(kcal)": [food_dict[v.name.replace("_", " ")]["Cals"] * v.varValue for v in
                                       model.variables()],
                        "Carbs(gr)": [food_dict[v.name.replace("_", " ")]["Carbs"] * v.varValue for v in
                                      model.variables()],
                        "Proteins(gr)": [food_dict[v.name.replace("_", " ")]["Proteins"] * v.varValue for v in
                                         model.variables()],
                        "Fats(gr)": [food_dict[v.name.replace("_", " ")]["Fats"] * v.varValue for v in
                                     model.variables()]}
                df = pd.DataFrame(dict)
                df.loc['Total'] = df.sum(numeric_only=True)
                st.dataframe(df)
                df.to_excel("my_meal_plan.xlsx")
                with open("my_meal_plan.xlsx", "rb") as f:
                    st.download_button("Download meal plan", f, file_name="my_meal_plan.xlsx")

            else:
                st.error(f"Solver error: status {status}")

    with st.expander("Calories/Fats proportions"):
        cals = st.number_input("Enter calories(kcal)", min_value=0., max_value=5000., step=1.)
        proteins = st.number_input("Enter proteins(gr)", min_value=0., max_value=500., step=1.)
        if st.button("Compute proportions"):
            st.divider()
            proteins_cal = proteins * 4
            proteins_ratio_cal = proteins_cal / cals
            ratios = [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]
            remaining_ratio_cal = 1. - proteins_ratio_cal
            arr = np.zeros((11, 3))
            df = pd.DataFrame(arr, columns=["Carbs-Proteins-Fats(%)", "Carbs-Proteins-Fats(kcal)",
                                            "Carbs-Proteins-Fats(gr)"]).astype(str)
            for ind, r in enumerate(ratios):
                df.loc[ind, "Carbs-Proteins-Fats(%)"] = f"{int((1-r) * remaining_ratio_cal * 100)}-{int(proteins_ratio_cal * 100)}-{int(r * remaining_ratio_cal * 100)}"
                df.loc[ind, "Carbs-Proteins-Fats(kcal)"] = f"{int((1-r) * remaining_ratio_cal * cals)}-{int(proteins_ratio_cal * cals)}-{int(r * remaining_ratio_cal * cals)}"
                df.loc[ind, "Carbs-Proteins-Fats(gr)"] = f"{int(((1 - r) * remaining_ratio_cal * cals)/4)}-{int((proteins_ratio_cal * cals)/4)}-{int((r * remaining_ratio_cal * cals)/9)}"

            st.dataframe(df)

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
                "Qnt(gr)": st.column_config.NumberColumn("Qnt(gr)", width="small", required=True, default=0,
                                                         format=None,
                                                         min_value=0, max_value=1000)
            },
            hide_index=True,
        )
        if st.button("Compute nutritional values"):
            dict = {
                "Food": [food_table["Food"][ind] for ind in food_table.index],
                "Qnt(gr)": [food_table["Qnt(gr)"][ind] for ind in food_table.index],
                "Cals(kcal)": [food_dict[food_table["Food"][ind]]["Cals"] * food_table["Qnt(gr)"][ind] for ind in
                               food_table.index],
                "Carbs(gr)": [food_dict[food_table["Food"][ind]]["Carbs"] * food_table["Qnt(gr)"][ind] for ind in
                              food_table.index],
                "Proteins(gr)": [food_dict[food_table["Food"][ind]]["Proteins"] * food_table["Qnt(gr)"][ind] for ind in
                                 food_table.index],
                "Fats(gr)": [food_dict[food_table["Food"][ind]]["Fats"] * food_table["Qnt(gr)"][ind] for ind in
                             food_table.index]
            }
            df = pd.DataFrame(dict)
            df.loc['Total'] = df.sum(numeric_only=True)
            st.dataframe(df)
            df.to_excel("my_meal_nutrition.xlsx")
            with open("my_meal_nutrition.xlsx", "rb") as f:
                st.download_button("Download meal nutrition", f, file_name="my_meal_nutrition.xlsx")

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

