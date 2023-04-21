import streamlit as st
import pickle
import pandas as pd
import utils

st.set_page_config(
    page_title="History",
    page_icon="📜",
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

AWS_BUCKET="fitnessmanagement/"

fs = utils.s3fs_file_system()
fs.clear_instance_cache()

st.write("# History! 📜")

EXERCISE_LIST_PATH = "exercises.txt"
with open(EXERCISE_LIST_PATH, 'rb') as f:
    exercise_list = [str(e, 'utf-8').strip() for e in f.readlines()]
    exercise_list.sort()
    exercise_list = ['<select>'] + exercise_list

st.markdown(
    """
    Check the history of an exercise.
    """
)

user = st.selectbox('Who is the user?', ('<select>', 'Alberto', 'Giuseppe'))
exercise = st.selectbox('What is the exercise?', exercise_list)

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
                        new_d[str(repetition) + " reps"] = [str(weight) + " Kg" for time, weight in d[repetition][exercise][::-1]]
                if len(new_d) != 0:
                    df = pd.DataFrame(new_d)
                    cols = df.columns.tolist()
                    cols.sort()
                    df = df[cols]
                    print(df)
                    st.dataframe(df)
                else:
                    st.error("Sorry, no results found!")
        else:
            st.error("Sorry, a database file does not exist!")
