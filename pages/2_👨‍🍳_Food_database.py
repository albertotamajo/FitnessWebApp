import pandas as pd
import streamlit as st
import requests
from streamlit_image_select import image_select
import pickle
import utils
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Food database",
    page_icon="👨‍🍳",
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

    st.write("# Food database! 👨‍🍳")
    with st.expander("""### Add food from openfoodfacts"""):
        query = st.text_input("Write a query for the food", value="", key="foodQuery")
        query = "+".join(query.split())
        url = "https://it.openfoodfacts.org/cgi/search.pl?search_terms={0}&search_simple=1&json=1&action=process"
        if query is not "":
            search_result = requests.get(url.format(query)).json()
            products = search_result['products'][:10]
            if len(products) is not 0:
                ind = image_select("Select food",
                                   [p["image_front_small_url"] for p in products if "image_front_small_url" in p],
                                   return_value="index", use_container_width=True)
                product = products[ind]
                product_name = " ".join((product["url"].split("/")[-1]).split("-"))
                calories = product["nutriments"]['energy-kcal_100g']
                carbs = product["nutriments"]['carbohydrates_100g']
                proteins = product["nutriments"]['proteins_100g']
                fats = product["nutriments"]['fat_100g']
                st.markdown(f"""## Food name """)
                food_name = st.text_input("", value=product_name)
                st.markdown(
                    f"""
                    ## Nutritional values
                    - Calories (100gr): :green[{calories}] kcal
                    - Carbs (100gr): :green[{carbs}] gr
                    - Proteins (100gr): :green[{proteins}] gr
                    - Fats (100gr): :green[{fats}] gr
                    """
                )
                if st.button('Add food', key="OpenFoodButton"):
                    save = True
                    if fs.exists(file):
                        with fs.open(file, 'rb') as f:
                            d = pickle.load(f)
                            if food_name not in d.keys():
                                d[food_name] = {"Cals": calories / 100.0, "Carbs": carbs / 100.0,
                                                "Proteins": proteins / 100.0,
                                                "Fats": fats / 100.0}
                            else:
                                save = False
                                st.error('Your food is already in the database')
                    else:
                        fs.touch(file)
                        d = {food_name: {"Cals": calories / 100.0, "Carbs": carbs / 100.0, "Proteins": proteins / 100.0,
                                         "Fats": fats / 100.0}}

                    if save:
                        if d:
                            with fs.open(file, 'wb') as f:
                                pickle.dump(d, f)
                                st.success("Food saved successfully!")
            else:
                st.error("There is no product matching the query!")

    with st.expander("""### Add food manually"""):
        food_name = st.text_input("Write the name of the food", value="", key="foodName")
        calories = st.number_input('Write the calories of this food (100gr)', min_value=0., max_value=1000., step=1.)
        carbs = st.number_input('Write the carbs of this food (100gr)', min_value=0., max_value=1000., step=1.)
        proteins = st.number_input('Write the proteins of this food (100gr)', min_value=0., max_value=1000., step=1.)
        fats = st.number_input('Write the fats of this food (100gr)', min_value=0., max_value=1000., step=1.)
        if st.button('Add food'):
            save = True
            if fs.exists(file):
                with fs.open(file, 'rb') as f:
                    d = pickle.load(f)
                    if food_name not in d.keys():
                        d[food_name] = {"Cals": calories / 100.0, "Carbs": carbs / 100.0, "Proteins": proteins / 100.0,
                                        "Fats": fats / 100.0}
                    else:
                        save = False
                        st.error('Your food is already in the database')
            else:
                fs.touch(file)
                d = {food_name: {"Cals": calories / 100.0, "Carbs": carbs / 100.0, "Proteins": proteins / 100.0,
                                 "Fats": fats / 100.0}}
            with fs.open(file, 'wb') as f:
                if save:
                    pickle.dump(d, f)
                    st.success("Food saved successfully!")

    with st.expander("""### Visualise food database"""):
        if fs.exists(file):
            with fs.open(file, 'rb') as f:
                d = pickle.load(f)
            df = pd.DataFrame({"Food": [i for i in d.keys()],
                               "Calories(100gr)": [d[i]["Cals"] * 100 for i in d.keys()],
                               "Carbs(100gr)": [d[i]["Carbs"] * 100 for i in d.keys()],
                               "Proteins(100gr)": [d[i]["Proteins"] * 100 for i in d.keys()],
                               "Fats(100gr)": [d[i]["Fats"] * 100 for i in d.keys()]
                               })
            st.dataframe(df)
        else:
            st.error("There is no food database at the moment")

    with st.expander("""### Remove food"""):
        if fs.exists(file):
            with fs.open(file, 'rb') as f:
                d = pickle.load(f)
            food = st.selectbox("Select the food to be removed", ["<select>"] + list(d.keys()))
            if st.button('Remove food'):
                if food is not "<select>":
                    d.pop(food)
                    with fs.open(file, 'wb') as f:
                        pickle.dump(d, f)
                        st.success("Food removed successfully!")
                else:
                    st.error("You need to select a food!")
        else:
            st.error("There is no food database at the moment")

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')