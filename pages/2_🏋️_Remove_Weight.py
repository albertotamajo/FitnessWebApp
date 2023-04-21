import streamlit as st
import pickle
import utils

st.set_page_config(
    page_title="Remove weight",
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

st.write("# Remove weight! 🏋️")

EXERCISE_LIST_PATH = "exercises.txt"

with open(EXERCISE_LIST_PATH, 'rb') as f:
    exercise_list = [str(e, 'utf-8').strip() for e in f.readlines()]
    exercise_list.sort()
    exercise_list = ['<select>'] + exercise_list

st.markdown(
    """
    Remove the weight you used for a given exercise.
    """
)

USER_KEY = "REMOVE_WEIGHT_USER_SELECTION"
EXERCISE_KEY = "REMOVE_WEIGHT_EXERCISE_SELECTION"
REPETITION_KEY = "REMOVE_WEIGHT_REPETITION_SELECTION"
PASSWORD_KEY = "ADD_WEIGHT_PASSWORD_SELECTION"
INDEX_KEY = "REMOVE_WEIGHT_INDEX_SELECTION"
repetition_default = 8


user = st.selectbox('Who is the user?', ('<select>', 'Alberto', 'Giuseppe'), key=USER_KEY)
exercise = st.selectbox('What is the exercise?', exercise_list, key=EXERCISE_KEY)
repetitions = st.slider('How many reps did you do?', 1, 20, value=repetition_default, key=REPETITION_KEY)
index = st.number_input('What is the index?', min_value=0, max_value=None, value=0, step=1, key=INDEX_KEY)
password = st.text_input('Password', key=PASSWORD_KEY)

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
        d = None
        if fs.exists(file):
            with fs.open(file, 'rb') as f:
                d = pickle.load(f)
                if repetitions in d.keys():
                    if exercise in d[repetitions].keys():
                        l = d[repetitions][exercise]
                        index_rev = len(l) - 1 - index
                        if len(l) > index_rev:
                            l.pop(index_rev)
                        else:
                            st.error("Sorry, the provided index does not exists!")
                    else:
                        st.error("Sorry, the exercise {0} does not have any entry for index {1}".format(exercise, index))
                else:
                    st.error("Sorry, there is no entry for repetition {0}".format(repetitions))
        if d is not None:
            with fs.open(file, 'wb') as f:
                pickle.dump(d, f)
            st.success('Weight removed successfully!')
