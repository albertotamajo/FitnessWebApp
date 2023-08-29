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

    with st.expander("Plan your diet"):
        st.markdown("""### :blue[Set diet objectives]""")
        daily_tab, breakfast_tab, snack1_tab, lunch_tab, snack2_tab, dinner_tab, snack3_tab = st.tabs(
            ["Daily", "Breakfast", "Snack1",
             "Lunch", "Snack2", "Dinner",
             "Snack3"])

        with daily_tab:
            cals, carbs, proteins, fats = st.columns(4)

            with cals:
                st.markdown("#### Calories")
                calsMax = st.number_input('Max', key="calsMax")
                calsMin = st.number_input('Min', key="calsMin")

            with carbs:
                st.markdown("#### Carbs")
                carbsMax = st.number_input('Max', key="carbsMax")
                carbsMin = st.number_input('Min', key="carbsMin")

            with proteins:
                st.markdown("#### Proteins")
                prtsMax = st.number_input('Max', key="prtsMax")
                prtsMin = st.number_input('Min', key="prtsMin")

            with fats:
                st.markdown("#### Fats")
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
        with breakfast_tab:
            cals_breakfast, carbs_breakfast, proteins_breakfast, fats_breakfast = st.columns(4)
            with cals_breakfast:
                st.markdown("#### Calories")
                calsMaxBreakfast = st.number_input('Max', value=10000., key="calsMaxBreakfast")
                calsMinBreakfast = st.number_input('Min', key="calsMinBreakfast")

            with carbs_breakfast:
                st.markdown("#### Carbs")
                carbsMaxBreakfast = st.number_input('Max', value=10000., key="carbsMaxBreakfast")
                carbsMinBreakfast = st.number_input('Min', key="carbsMinBreakfast")

            with proteins_breakfast:
                st.markdown("#### Proteins")
                prtsMaxBreakfast = st.number_input('Max', value=10000., key="prtsMaxBreakfast")
                prtsMinBreakfast = st.number_input('Min', key="prtsMinBreakfast")

            with fats_breakfast:
                st.markdown("#### Fats")
                fatsMaxBreakfast = st.number_input('Max', value=10000., key="fatsMaxBreakfast")
                fatsMinBreakfast = st.number_input('Min', key="fatsMinBreakfast")
        with snack1_tab:
            cals_snack1, carbs_snack1, proteins_snack1, fats_snack1 = st.columns(4)
            with cals_snack1:
                st.markdown("#### Calories")
                calsMaxSnack1 = st.number_input('Max', value=10000., key="calsMaxSnack1")
                calsMinSnack1 = st.number_input('Min', key="calsMinSnack1")

            with carbs_snack1:
                st.markdown("#### Carbs")
                carbsMaxSnack1 = st.number_input('Max', value=10000., key="carbsMaxSnack1")
                carbsMinSnack1 = st.number_input('Min', key="carbsMinSnack1")

            with proteins_snack1:
                st.markdown("#### Proteins")
                prtsMaxSnack1 = st.number_input('Max', value=10000., key="prtsMaxSnack1")
                prtsMinSnack1 = st.number_input('Min', key="prtsMinSnack1")

            with fats_snack1:
                st.markdown("#### Fats")
                fatsMaxSnack1 = st.number_input('Max', value=10000., key="fatsMaxSnack1")
                fatsMinSnack1 = st.number_input('Min', key="fatsMinSnack1")
        with lunch_tab:
            cals_lunch, carbs_lunch, proteins_lunch, fats_lunch = st.columns(4)
            with cals_lunch:
                st.markdown("#### Calories")
                calsMaxLunch = st.number_input('Max', value=10000., key="calsMaxLunch")
                calsMinLunch = st.number_input('Min', key="calsMinLunch")

            with carbs_lunch:
                st.markdown("#### Carbs")
                carbsMaxLunch = st.number_input('Max', value=10000., key="carbsMaxLunch")
                carbsMinLunch = st.number_input('Min', key="carbsMinLunch")

            with proteins_lunch:
                st.markdown("#### Proteins")
                prtsMaxLunch = st.number_input('Max', value=10000., key="prtsMaxLunch")
                prtsMinLunch = st.number_input('Min', key="prtsMinLunch")

            with fats_lunch:
                st.markdown("#### Fats")
                fatsMaxLunch = st.number_input('Max', value=10000., key="fatsMaxLunch")
                fatsMinLunch = st.number_input('Min', key="fatsMinLunch")
        with snack2_tab:
            cals_snack2, carbs_snack2, proteins_snack2, fats_snack2 = st.columns(4)
            with cals_snack2:
                st.markdown("#### Calories")
                calsMaxSnack2 = st.number_input('Max', value=10000., key="calsMaxSnack2")
                calsMinSnack2 = st.number_input('Min', key="calsMinSnack2")

            with carbs_snack2:
                st.markdown("#### Carbs")
                carbsMaxSnack2 = st.number_input('Max', value=10000., key="carbsMaxSnack2")
                carbsMinSnack2 = st.number_input('Min', key="carbsMinSnack2")

            with proteins_snack2:
                st.markdown("#### Proteins")
                prtsMaxSnack2 = st.number_input('Max', value=10000., key="prtsMaxSnack2")
                prtsMinSnack2 = st.number_input('Min', key="prtsMinSnack2")

            with fats_snack2:
                st.markdown("#### Fats")
                fatsMaxSnack2 = st.number_input('Max', value=10000., key="fatsMaxSnack2")
                fatsMinSnack2 = st.number_input('Min', key="fatsMinSnack2")
        with dinner_tab:
            cals_dinner, carbs_dinner, proteins_dinner, fats_dinner = st.columns(4)
            with cals_dinner:
                st.markdown("#### Calories")
                calsMaxDinner = st.number_input('Max', value=10000., key="calsMaxDinner")
                calsMinDinner = st.number_input('Min', key="calsMinDinner")

            with carbs_dinner:
                st.markdown("#### Carbs")
                carbsMaxDinner = st.number_input('Max', value=10000., key="carbsMaxDinner")
                carbsMinDinner = st.number_input('Min', key="carbsMinDinner")

            with proteins_dinner:
                st.markdown("#### Proteins")
                prtsMaxDinner = st.number_input('Max', value=10000., key="prtsMaxDinner")
                prtsMinDinner = st.number_input('Min', key="prtsMinDinner")

            with fats_dinner:
                st.markdown("#### Fats")
                fatsMaxDinner = st.number_input('Max', value=10000., key="fatsMaxDinner")
                fatsMinDinner = st.number_input('Min', key="fatsMinDinner")
        with snack3_tab:
            cals_snack3, carbs_snack3, proteins_snack3, fats_snack3 = st.columns(4)
            with cals_snack3:
                st.markdown("#### Calories")
                calsMaxSnack3 = st.number_input('Max', value=10000., key="calsMaxSnack3")
                calsMinSnack3 = st.number_input('Min', key="calsMinSnack3")

            with carbs_snack3:
                st.markdown("#### Carbs")
                carbsMaxSnack3 = st.number_input('Max', value=10000., key="carbsMaxSnack3")
                carbsMinSnack3 = st.number_input('Min', key="carbsMinSnack3")

            with proteins_snack3:
                st.markdown("#### Proteins")
                prtsMaxSnack3 = st.number_input('Max', value=10000., key="prtsMaxSnack3")
                prtsMinSnack3 = st.number_input('Min', key="prtsMinSnack3")

            with fats_snack3:
                st.markdown("#### Fats")
                fatsMaxSnack3 = st.number_input('Max', value=10000., key="fatsMaxSnack3")
                fatsMinSnack3 = st.number_input('Min', key="fatsMinSnack3")

        st.divider()

        st.markdown("""### :blue[Select food]""")

        convert_dict = {'Food': str,
                        'Meal': str,
                        'Min(gr)': int,
                        'Max(gr)': int
                        }
        data_df = pd.DataFrame(
            {
                "Food": [],
                "Meal": [],
                "Min(gr)": [],
                "Max(gr)": []
            }
        ).astype(convert_dict)

        food_dict = fetch_food()
        meals = ["None", "Breakfast", "Snack1", "Lunch", "Snack2", "Dinner", "Snack3"]

        food_table = st.data_editor(
            data_df,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Food": st.column_config.SelectboxColumn(
                    "Food",
                    width="medium",
                    options=list(food_dict.keys()),
                    required=True,
                ),
                "Meal": st.column_config.SelectboxColumn(
                    "Meal",
                    width="medium",
                    default="None",
                    options=meals,
                    required=True,
                ),
                "Min(gr)": st.column_config.NumberColumn("Min(gr)", width="small", required=True, default=0,
                                                         format=None,
                                                         min_value=0, max_value=1000),
                "Max(gr)": st.column_config.NumberColumn("Max(gr)", width="small", required=True, default=1000,
                                                         format=None,
                                                         min_value=0, max_value=1000)
            },
            hide_index=True,
        )
        st.divider()
        st.markdown("""### :blue[Optimisation choices]""")
        calsOpt, carbsOpt, proteinsOpt, fatsOpt = st.columns(4)
        options = ["None", "Maximise", "Minimise"]
        with calsOpt:
            st.markdown("#### Calories")
            calsDec = st.selectbox("", options=options, key="calsDec")

        with carbsOpt:
            st.markdown("#### Carbs")
            carbsDec = st.selectbox("", options=options, key="carbsDec")

        with proteinsOpt:
            st.markdown("#### Proteins")
            proteinsDec = st.selectbox("", options=options, key="proteinsDec")

        with fatsOpt:
            st.markdown("#### Fats")
            fatsDec = st.selectbox("", options=options, key="fatsDec")

        st.divider()
        if st.button("Compute meal plan"):
            if calsDec == "None":
                calsCoef = np.asarray([0. for ind in food_table.index])
            else:
                calsCoef = np.asarray([food_dict[food_table["Food"][ind]]["Cals"] for ind in food_table.index])
                if calsDec == "Minimise":
                    calsCoef = - calsCoef

            if carbsDec is "None":
                carbsCoef = np.asarray([0. for ind in food_table.index])
            else:
                carbsCoef = np.asarray([food_dict[food_table["Food"][ind]]["Carbs"] for ind in food_table.index])
                if carbsDec == "Minimise":
                    carbsCoef = - carbsCoef

            if proteinsDec is "None":
                proteinsCoef = np.asarray([0. for ind in food_table.index])
            else:
                proteinsCoef = np.asarray([food_dict[food_table["Food"][ind]]["Proteins"] for ind in food_table.index])
                if proteinsDec == "Minimise":
                    proteinsCoef = - proteinsCoef

            if fatsDec is "None":
                fatsCoef = np.asarray([0. for ind in food_table.index])
            else:
                fatsCoef = np.asarray([food_dict[food_table["Food"][ind]]["Fats"] for ind in food_table.index])
                if fatsDec == "Minimise":
                    fatsCoef = - fatsCoef

            coef = calsCoef + carbsCoef + proteinsCoef + fatsCoef
            if not np.any(coef):
                coef = coef + 1.

            # Instantiate model
            model = LpProblem("MealPlan", LpMaximize)
            # Instantiate decision variables
            decision_variables = [LpVariable(name=food_table["Food"][ind] + "_" + food_table["Meal"][ind], lowBound=food_table["Min(gr)"][ind],
                                             upBound=food_table["Max(gr)"][ind], cat=LpInteger) for ind in
                                  food_table.index]
            # Add Objective function
            model += lpSum([decision_variables[ind] * float(c) for ind, c in enumerate(coef)])

            # Add daily constraints
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

            dec_var_names = [v.name for v in decision_variables]

            # Add snack1 constraints
            if np.any(np.asarray(["Sn" in v for v in dec_var_names])):
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in food_table.index
                     if "Breakfast" in decision_variables[ind].name]) \
                         >= calsMinBreakfast, "minCaloriesBreakfast"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in food_table.index
                     if "Breakfast" in decision_variables[ind].name]) \
                         <= calsMaxBreakfast, "maxCaloriesBreakfast"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in food_table.index
                     if "Breakfast" in decision_variables[ind].name]) \
                         >= carbsMinBreakfast, "minCarbsBreakfast"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in food_table.index
                     if "Breakfast" in decision_variables[ind].name]) \
                         <= carbsMaxBreakfast, "maxCarbsBreakfast"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in food_table.index
                     if "Breakfast" in decision_variables[ind].name]) \
                         >= prtsMinBreakfast, "minProteinsBreakfast"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in food_table.index
                     if "Breakfast" in decision_variables[ind].name]) \
                         <= prtsMaxBreakfast, "maxProteinsBreakfast"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in food_table.index
                     if "Breakfast" in decision_variables[ind].name]) \
                         >= fatsMinBreakfast, "minFatsBreakfast"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in food_table.index
                     if "Breakfast" in decision_variables[ind].name]) \
                         <= fatsMaxBreakfast, "maxFatsBreakfast"

            # Add snack1 constraints
            if np.any(np.asarray(["Snack1" in v for v in dec_var_names])):
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Snack1" in decision_variables[ind].name]) \
                         >= calsMinSnack1, "minCaloriesSnack1"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Snack1" in decision_variables[ind].name]) \
                         <= calsMaxSnack1, "maxCaloriesSnack1"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Snack1" in decision_variables[ind].name]) \
                         >= carbsMinSnack1, "minCarbsSnack1"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Snack1" in decision_variables[ind].name]) \
                         <= carbsMaxSnack1, "maxCarbsSnack1"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Snack1" in decision_variables[ind].name]) \
                         >= prtsMinSnack1, "minProteinsSnack1"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Snack1" in decision_variables[ind].name]) \
                         <= prtsMaxSnack1, "maxProteinsSnack1"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Snack1" in decision_variables[ind].name]) \
                         >= fatsMinSnack1, "minFatsSnack1"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Snack1" in decision_variables[ind].name]) \
                         <= fatsMaxSnack1, "maxFatsSnack1"

            # Add snack2 constraints
            if np.any(np.asarray(["Snack2" in v for v in dec_var_names])):
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Snack2" in decision_variables[ind].name]) \
                         >= calsMinSnack2, "minCaloriesSnack2"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Snack2" in decision_variables[ind].name]) \
                         <= calsMaxSnack2, "maxCaloriesSnack2"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Snack2" in decision_variables[ind].name]) \
                         >= carbsMinSnack2, "minCarbsSnack2"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Snack2" in decision_variables[ind].name]) \
                         <= carbsMaxSnack2, "maxCarbsSnack2"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Snack2" in decision_variables[ind].name]) \
                         >= prtsMinSnack2, "minProteinsSnack2"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Snack2" in decision_variables[ind].name]) \
                         <= prtsMaxSnack2, "maxProteinsSnack2"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Snack2" in decision_variables[ind].name]) \
                         >= fatsMinSnack2, "minFatsSnack2"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Snack2" in decision_variables[ind].name]) \
                         <= fatsMaxSnack2, "maxFatsSnack2"

            # Add snack3 constraints
            if np.any(np.asarray(["Snack3" in v for v in dec_var_names])):
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Snack3" in decision_variables[ind].name]) \
                         >= calsMinSnack3, "minCaloriesSnack3"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Snack3" in decision_variables[ind].name]) \
                         <= calsMaxSnack3, "maxCaloriesSnack3"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Snack3" in decision_variables[ind].name]) \
                         >= carbsMinSnack3, "minCarbsSnack3"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Snack3" in decision_variables[ind].name]) \
                         <= carbsMaxSnack3, "maxCarbsSnack3"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Snack3" in decision_variables[ind].name]) \
                         >= prtsMinSnack3, "minProteinsSnack3"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Snack3" in decision_variables[ind].name]) \
                         <= prtsMaxSnack3, "maxProteinsSnack3"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Snack3" in decision_variables[ind].name]) \
                         >= fatsMinSnack3, "minFatsSnack3"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Snack3" in decision_variables[ind].name]) \
                         <= fatsMaxSnack3, "maxFatsSnack3"

            # Add lunch constraints
            if np.any(np.asarray(["Lunch" in v for v in dec_var_names])):
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Lunch" in decision_variables[ind].name]) \
                         >= calsMinLunch, "minCaloriesLunch"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Lunch" in decision_variables[ind].name]) \
                         <= calsMaxLunch, "maxCaloriesLunch"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Lunch" in decision_variables[ind].name]) \
                         >= carbsMinLunch, "minCarbsLunch"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Lunch" in decision_variables[ind].name]) \
                         <= carbsMaxLunch, "maxCarbsLunch"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Lunch" in decision_variables[ind].name]) \
                         >= prtsMinLunch, "minProteinsLunch"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Lunch" in decision_variables[ind].name]) \
                         <= prtsMaxLunch, "maxProteinsLunch"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Lunch" in decision_variables[ind].name]) \
                         >= fatsMinLunch, "minFatsLunch"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Lunch" in decision_variables[ind].name]) \
                         <= fatsMaxLunch, "maxFatsLunch"

            # Add dinner constraints
            if np.any(np.asarray(["Dinner" in v for v in dec_var_names])):
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Dinner" in decision_variables[ind].name]) \
                         >= calsMinDinner, "minCaloriesDinner"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Cals"] for ind in
                     food_table.index
                     if "Dinner" in decision_variables[ind].name]) \
                         <= calsMaxDinner, "maxCaloriesDinner"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Dinner" in decision_variables[ind].name]) \
                         >= carbsMinDinner, "minCarbsDinner"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Carbs"] for ind in
                     food_table.index
                     if "Dinner" in decision_variables[ind].name]) \
                         <= carbsMaxDinner, "maxCarbsDinner"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Dinner" in decision_variables[ind].name]) \
                         >= prtsMinDinner, "minProteinsDinner"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Proteins"] for ind in
                     food_table.index
                     if "Dinner" in decision_variables[ind].name]) \
                         <= prtsMaxDinner, "maxProteinsDinner"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Dinner" in decision_variables[ind].name]) \
                         >= fatsMinDinner, "minFatsDinner"
                model += lpSum(
                    [decision_variables[ind] * food_dict[food_table["Food"][ind]]["Fats"] for ind in
                     food_table.index
                     if "Dinner" in decision_variables[ind].name]) \
                         <= fatsMaxDinner, "maxFatsDinner"

            # The problem is solved using PuLP's Solver
            status = LpStatus[model.solve()]
            st.divider()
            if status is "Optimal":
                dict = {"Food": [" ".join(v.name.replace("_", " ").split()[:-1]) for v in model.variables()],
                        "Meal": [v.name.split("_")[-1] for v in model.variables()],
                        "Qnt(gr)": [v.varValue for v in model.variables()],
                        "Cals(kcal)": [food_dict[" ".join(v.name.replace("_", " ").split()[:-1])]["Cals"] * v.varValue
                                       for v in model.variables()],
                        "Carbs(gr)": [food_dict[" ".join(v.name.replace("_", " ").split()[:-1])]["Carbs"] * v.varValue
                                      for v in model.variables()],
                        "Proteins(gr)": [food_dict[" ".join(v.name.replace("_", " ").split()[:-1])]["Proteins"] * v.varValue
                                         for v in model.variables()],
                        "Fats(gr)": [food_dict[" ".join(v.name.replace("_", " ").split()[:-1])]["Fats"] * v.varValue
                                     for v in model.variables()]}
                df = pd.DataFrame(dict)
                df.loc['Total'] = df.sum(numeric_only=True)
                df.loc['% kcal'] = (df.loc['Total'] / df.loc['Total']["Cals(kcal)"]) * np.asarray([0,0,0,0,4,4,9])
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

