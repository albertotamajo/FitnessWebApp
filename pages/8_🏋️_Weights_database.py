import streamlit as st
import pickle
import pytz
from datetime import datetime
import utils
import pandas as pd

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

AWS_BUCKET = "fitnessmanagement/"

fs = utils.s3fs_file_system()
fs.clear_instance_cache()

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
    password = st.text_input('Password', key=ADD_PASSWORD_KEY)
    if st.button('Add weight'):
        if user == '<select>' or exercise == '<select>' or password != st.secrets["PASSWORD"]:
            if user == '<select>':
                st.error('You need to select a user')
            if exercise == '<select>':
                st.error('You need to select an exercise')
            if password != st.secrets["PASSWORD"]:
                st.error('You need to type a correct password')
        else:
            datetime = datetime.now(pytz.timezone("Europe/Rome"))
            date = "{0}-{1}-{2}".format(datetime.year, datetime.month, datetime.day)
            d = {repetitions: {exercise: [(date, weight)]}}
            file = "{0}Weights{1}.pickle".format(AWS_BUCKET, user)
            if fs.exists(file):
                with fs.open(file, 'rb') as f:
                    d = pickle.load(f)
                    if repetitions in d.keys():
                        if exercise in d[repetitions].keys():
                            d[repetitions][exercise].append((date, weight))
                        else:
                            d[repetitions][exercise] = [(date, weight)]
                    else:
                        d[repetitions] = {exercise: [(date, weight)]}
            else:
                fs.touch(file)
            with fs.open(file, 'wb') as f:
                pickle.dump(d, f)

            filecopy = "{0}Weights{1}(Copy).pickle".format(AWS_BUCKET, user)
            if not fs.exists(filecopy):
                fs.touch(filecopy)
            with fs.open(filecopy, 'wb') as f:
                pickle.dump(d, f)
            st.success('Weight added successfully!')

with st.expander("Remove weights"):
    user = st.selectbox('Who is the user?', ('<select>', 'Alberto', 'Giuseppe'), key=REMOVE_USER_KEY)
    exercise = st.selectbox('What is the exercise?', exercise_list, key=REMOVE_EXERCISE_KEY)
    repetitions = st.slider('How many reps did you do?', 1, 20, value=repetition_default, key=REMOVE_REPETITION_KEY)
    index = st.number_input('What is the index?', min_value=0, max_value=None, value=0, step=1, key=REMOVE_INDEX_KEY)
    password = st.text_input('Password', key=REMOVE_PASSWORD_KEY)

    if st.button('Remove weight'):
        if user == '<select>' or exercise == '<select>' or password != st.secrets["PASSWORD"]:
            if user == '<select>':
                st.error('You need to select a user')
            if exercise == '<select>':
                st.error('You need to select an exercise')
            if password != st.secrets["PASSWORD"]:
                st.error('You need to type a correct password')
        else:
            file = "{0}Weights{1}.pickle".format(AWS_BUCKET, user)
            remove = False
            if fs.exists(file):
                with fs.open(file, 'rb') as f:
                    d = pickle.load(f)
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
                                "Sorry, the exercise {0} does not have any entry for index {1}".format(exercise, index))
                    else:
                        st.error("Sorry, there is no entry for repetition {0}".format(repetitions))
                if remove:
                    with fs.open(file, 'wb') as f:
                        pickle.dump(d, f)
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
            file = "{0}Weights{1}.pickle".format(AWS_BUCKET, user)
            if fs.exists(file):
                with fs.open(file, 'rb') as f:
                    d = pickle.load(f)
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