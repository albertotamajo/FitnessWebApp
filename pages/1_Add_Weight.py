import streamlit as st
import pickle
import pytz
import s3fs
from datetime import datetime

st.set_page_config(
    page_title="Add weight",
    page_icon="❚█══█❚",
)
AWS_BUCKET="fitnessmanagement/"

fs = s3fs.S3FileSystem(anon=False)
print(fs.ls("fitnessmanagement/"))


st.write("# Add weight! ❚█══█❚")

EXERCISE_LIST_PATH = "exercises.txt"
with open(EXERCISE_LIST_PATH, 'rb') as f:
    exercise_list = [str(e, 'utf-8') for e in f.readlines()]
    exercise_list.sort()
    exercise_list = ['<select>'] + exercise_list

st.markdown(
    """
    Record the weight you used for a given exercise.
    """
)

user = st.selectbox('Who is the user?', ('<select>', 'Alberto', 'Giuseppe'))
exercise = st.selectbox('What is the exercise?', exercise_list)
repetitions = st.slider('How many reps did you do?', 1, 20, value=8)
weight = st.number_input('What weight did you use (kg)?', min_value=0.0, max_value=200.0, value=50.0, step=0.25)
password = st.text_input('Password')
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
        d = {exercise: [(date, weight)]}
        file = "{0}AddWeight{1}-{2}.pickle".format(AWS_BUCKET, user, repetitions)
        if fs.exists(file):
            with fs.open(file, 'rb') as f:
                d = pickle.load(f)
                if exercise in d.keys():
                    d[exercise].append((date, weight))
                else:
                    d[exercise] = [(date, weight)]
        else:
            fs.touch(file)
        with fs.open(file, 'wb') as f:
            pickle.dump(d, f)
        st.success('Weight added successfully!')