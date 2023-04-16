import streamlit as st
import pickle
import os
import s3fs
import Home

fs = s3fs.S3FileSystem(anon=False)

st.set_page_config(
    page_title="Add weight",
    page_icon="❚█══█❚",
)

st.write("# Add weight! ❚█══█❚")

EXERCISE_LIST_PATH = "exercises.pickle"
with open(EXERCISE_LIST_PATH, 'rb') as f:
    exercise_list = pickle.load(f)
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
if st.button('Add weight'):
    if user == '<select>' or exercise == '<select>':
        if user == '<select>':
            st.error('You need to select a user')
        if exercise == '<select>':
            st.error('You need to select an exercise')
    else:
        d = {exercise: weight}
        file = "{0}AddWeight{1}-{2}.pickle".format(Home.AWS_BUCKET, user, repetitions)
        if os.path.exists(file):
            with open(file, 'rb') as f:
                d = pickle.load(f)
                if exercise in d.keys():
                    d[exercise].append(weight)
                else:
                    d[exercise] = [weight]
        with open(file, 'wb') as f:
            pickle.dump(d, f)
        st.success('Weight added successfully!')