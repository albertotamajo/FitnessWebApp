import streamlit as st
import pickle
import pytz
from datetime import datetime
import utils
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils import dropbox_connect, dropbox_download_file, dropbox_file_exists, dropbox_upload_file

st.set_page_config(
    page_title="Weights database",
    page_icon="🏋️",
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
    dbx = dropbox_connect()
    st.write("# Weights database! 🏋️")
    EXERCISE_LIST_PATH = "exercises.txt"

    with open(EXERCISE_LIST_PATH, 'rb') as f:
        exercise_list = [str(e, 'utf-8').strip() for e in f.readlines()]
        exercise_list.sort()
        exercise_list = ['<select>'] + exercise_list

    ADD_USER_KEY = "ADD_WEIGHT_USER_SELECTION"
    ADD_EXERCISE_KEY = "ADD_WEIGHT_EXERCISE_SELECTION"
    ADD_REPETITION_KEY = "ADD_WEIGHT_REPETITION_SELECTION"
    ADD_WEIGHT_KEY = "ADD_WEIGHT_WEIGHT_SELECTION"
    ADD_PASSWORD_KEY = "ADD_WEIGHT_PASSWORD_SELECTION"

    REMOVE_USER_KEY = "REMOVE_WEIGHT_USER_SELECTION"
    REMOVE_EXERCISE_KEY = "REMOVE_WEIGHT_EXERCISE_SELECTION"
    REMOVE_REPETITION_KEY = "REMOVE_WEIGHT_REPETITION_SELECTION"
    REMOVE_PASSWORD_KEY = "REMOVE_WEIGHT_PASSWORD_SELECTION"
    REMOVE_INDEX_KEY = "REMOVE_WEIGHT_INDEX_SELECTION"

    HISTORY_USER_KEY = "HISTORY_USER_SELECTION"
    HISTORY_EXERCISE_KEY = "HISTORY_EXERCISE_SELECTION"

    repetition_default = 8
    weight_default = 50.0

    with st.expander("Add weights"):
        user = st.selectbox('Who is the user?', ('<select>', 'Alberto', 'Giuseppe'), key=ADD_USER_KEY)
        exercise = st.selectbox('What is the exercise?', exercise_list, key=ADD_EXERCISE_KEY)
        repetitions = st.slider('How many reps did you do?', 1, 20, value=repetition_default, key=ADD_REPETITION_KEY)
        weight = st.number_input('What weight did you use (kg)?', min_value=0.0, max_value=200.0, value=weight_default,
                                 step=0.25, key=ADD_WEIGHT_KEY)
        if st.button('Add weight'):
            if user == '<select>' or exercise == '<select>':
                if user == '<select>':
                    st.error('You need to select a user')
                if exercise == '<select>':
                    st.error('You need to select an exercise')
            else:
                datetime = datetime.now(pytz.timezone("Europe/Rome"))
                date = "{0}-{1}-{2}".format(datetime.year, datetime.month, datetime.day)
                d = {repetitions: {exercise: [(date, weight)]}}
                file = f"/Weights{user}.pickle"
                if dropbox_file_exists(dbx, "", file[1:]):
                    d = dropbox_download_file(dbx, file)
                    if repetitions in d.keys():
                        if exercise in d[repetitions].keys():
                            d[repetitions][exercise].append((date, weight))
                        else:
                            d[repetitions][exercise] = [(date, weight)]
                    else:
                        d[repetitions] = {exercise: [(date, weight)]}
                dropbox_upload_file(dbx, d, file)
                st.success('Weight added successfully!')

    with st.expander("Remove weights"):
        user = st.selectbox('Who is the user?', ('<select>', 'Alberto', 'Giuseppe'), key=REMOVE_USER_KEY)
        exercise = st.selectbox('What is the exercise?', exercise_list, key=REMOVE_EXERCISE_KEY)
        repetitions = st.slider('How many reps did you do?', 1, 20, value=repetition_default, key=REMOVE_REPETITION_KEY)
        index = st.number_input('What is the index?', min_value=0, max_value=None, value=0, step=1,
                                key=REMOVE_INDEX_KEY)

        if st.button('Remove weight'):
            if user == '<select>' or exercise == '<select>':
                if user == '<select>':
                    st.error('You need to select a user')
                if exercise == '<select>':
                    st.error('You need to select an exercise')
            else:
                file = f"/Weights{user}.pickle"
                remove = False
                if dropbox_file_exists(dbx, "", file[1:]):
                    d = dropbox_download_file(dbx, file)
                    if repetitions in d.keys():
                        if exercise in d[repetitions].keys():
                            l = d[repetitions][exercise]
                            index_rev = len(l) - 1 - index
                            if len(l) > index_rev:
                                l.pop(index_rev)
                                if len(l) == 0:
                                    del d[repetitions][exercise]
                                if len(d[repetitions]) == 0:
                                    del d[repetitions]
                                remove = True
                            else:
                                st.error("Sorry, the provided index does not exists!")
                        else:
                            st.error(
                                "Sorry, the exercise {0} does not have any entry for index {1}".format(exercise,
                                                                                                       index))
                    else:
                        st.error("Sorry, there is no entry for repetition {0}".format(repetitions))
                if remove:
                    dropbox_upload_file(dbx, d, file)
                    st.success('Weight removed successfully!')

    with st.expander("History"):
        user = st.selectbox('Who is the user?', ('<select>', 'Alberto', 'Giuseppe'), key=HISTORY_USER_KEY)
        exercise = st.selectbox('What is the exercise?', exercise_list, key=HISTORY_EXERCISE_KEY)

        if st.button('Check'):
            if user == '<select>' or exercise == '<select>':
                if user == '<select>':
                    st.error('You need to select a user')
                if exercise == '<select>':
                    st.error('You need to select an exercise')
            else:
                file = f"/Weights{user}.pickle"
                if dropbox_file_exists(dbx, "", file[1:]):
                    d = dropbox_download_file(dbx, file)
                    new_d = {}
                    for repetition in d.keys():
                        if exercise in d[repetition].keys():
                            new_d[str(repetition) + " reps"] = [str(weight) + " Kg" for time, weight in
                                                                d[repetition][exercise][::-1]]
                    if len(new_d) != 0:
                        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in new_d.items()]))
                        cols = df.columns.tolist()
                        cols.sort()
                        df = df[cols]
                        print(df)
                        st.dataframe(df)
                    else:
                        st.error("Sorry, no results found!")
                else:
                    st.error("Sorry, a database file does not exist!")

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
