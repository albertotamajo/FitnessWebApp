import streamlit as st
import s3fs

@st.cache_resource
def s3fs_file_system():
    return s3fs.S3FileSystem(anon=False)

