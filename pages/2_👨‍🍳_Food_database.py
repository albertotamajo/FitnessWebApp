import pandas as pd
import streamlit as st
import requests
from streamlit_image_select import image_select
from utils import dropbox_connect, dropbox_download_file, dropbox_upload_file, dropbox_file_exists
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

    @st.cache_data(ttl="15m")
    def fetch_food():
        # Fetch data from URL here, and then clean it up.
        if dropbox_file_exists(dbx, "", file[1:]):
            return dropbox_download_file(dbx, file)
        else:
            return {}

    with st.sidebar:
        if st.button("Clear cache"):
            fetch_food.clear()
    authenticator.logout('Logout', 'sidebar')
    file = "/Food.pickle"
    dbx = dropbox_connect()

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
                calories = float(product["nutriments"]['energy-kcal_100g'])
                carbs = float(product["nutriments"]['carbohydrates_100g'])
                proteins = float(product["nutriments"]['proteins_100g'])
                fats = float(product["nutriments"]['fat_100g'])
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
                    if dropbox_file_exists(dbx, "", file[1:]):
                        d = dropbox_download_file(dbx, file)
                        if food_name not in d.keys():
                            d[food_name.strip()] = {"Cals": calories / 100.0, "Carbs": carbs / 100.0,
                                            "Proteins": proteins / 100.0,
                                            "Fats": fats / 100.0}
                        else:
                            save = False
                            st.error('Your food is already in the database')
                    else:
                        d = {food_name.strip(): {"Cals": calories / 100.0, "Carbs": carbs / 100.0, "Proteins": proteins / 100.0,
                                         "Fats": fats / 100.0}}
                    if save:
                        if d:
                            dropbox_upload_file(dbx, d, file)
                            fetch_food.clear()
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
            if dropbox_file_exists(dbx, "", file[1:]):
                d = dropbox_download_file(dbx, file)
                if food_name not in d.keys():
                    d[food_name.strip()] = {"Cals": calories / 100.0, "Carbs": carbs / 100.0, "Proteins": proteins / 100.0,
                                    "Fats": fats / 100.0}
                else:
                    save = False
                    st.error('Your food is already in the database')
            else:
                d = {food_name.strip(): {"Cals": calories / 100.0, "Carbs": carbs / 100.0, "Proteins": proteins / 100.0,
                                 "Fats": fats / 100.0}}
            if save:
                if d:
                    dropbox_upload_file(dbx, d, file)
                    fetch_food.clear()
                    st.success("Food saved successfully!")

    with st.expander("""### Visualise food database"""):
        d = fetch_food()
        if d:
            df = pd.DataFrame({"Food": [i for i in d.keys()],
                               "Calories(100gr)": [d[i]["Cals"] * 100 for i in d.keys()],
                               "Carbs(100gr)": [d[i]["Carbs"] * 100 for i in d.keys()],
                               "Proteins(100gr)": [d[i]["Proteins"] * 100 for i in d.keys()],
                               "Fats(100gr)": [d[i]["Fats"] * 100 for i in d.keys()]
                               })
            df = df.sort_values("Food")
            df.reset_index(inplace=True, drop=True)
            st.dataframe(df)
        else:
            st.error("There is no food database at the moment")

    with st.expander("""### Remove food"""):
        d = fetch_food()
        if d:
            food_list = list(d.keys())
            food_list.sort()
            food = st.selectbox("Select the food to be removed", ["<select>"] + food_list)
            if st.button('Remove food'):
                if food is not "<select>":
                    fetch_food.clear()
                    d = fetch_food()
                    d.pop(food)
                    dropbox_upload_file(dbx, d, file)
                    st.success("Food removed successfully!")
                else:
                    st.error("You need to select a food!")
        else:
            st.error("There is no food database at the moment")

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')