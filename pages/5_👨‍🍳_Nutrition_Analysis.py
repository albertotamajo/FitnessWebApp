import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Nutrition analysis",
    page_icon="👨‍🍳",
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


st.write("# Nutrition analysis! 👨‍🍳")

st.markdown(
    """
    Analyse the nutritional values of your food.
    """
)
edamam_app_id = st.secrets["EDAMAM_APP_ID"]
edamam_app_key = st.secrets["EDAMAM_APP_KEY"]
endpoint = "https://api.edamam.com/api/nutrition-data?app_id={0}&app_key={1}&nutrition-type=cooking&ingr={2}"\
    .format(edamam_app_id, edamam_app_key, "{0}")
food = st.text_area("Write your food here. One food per line.", value="")
password = st.text_input('Password')

if st.button('Analyse food'):
    if password != st.secrets["PASSWORD"] or food == "":
        if password != st.secrets["PASSWORD"]:
            st.error('You need to type a correct password')
        if food != "":
            st.error('You need to write some food')
    else:
        food_list = []
        quantity_list = []
        cals_list = []
        fats_list = []
        protiens_list = []
        carbs_list = []
        for f in food.replace(" ", "%20").splitlines():
            nutrition_dict = requests.get(endpoint.format(f)).json()
            food_list.append(nutrition_dict["ingredients"][0]["parsed"][0]["food"])
            quantity_list.append(nutrition_dict["ingredients"][0]["parsed"][0]["quantity"])
            nutrition_dict = nutrition_dict["totalNutrients"]
            cals_list.append(nutrition_dict["ENERC_KCAL"]["quantity"])
            fats_list.append(nutrition_dict["FAT"]["quantity"])
            protiens_list.append(nutrition_dict["PROCNT"]["quantity"])
            carbs_list.append(nutrition_dict["CHOCDF"]["quantity"])
        df = pd.DataFrame({"Food": food_list, "Quantity(gr)": quantity_list, "Calories": cals_list, "Carbs": carbs_list, "Fats": fats_list,
                                   "Proteins": protiens_list})
        df = df.append(df.sum(numeric_only=True), ignore_index=True).fillna("").rename({df.index[-1]: "Total"})
        st.dataframe(df)
