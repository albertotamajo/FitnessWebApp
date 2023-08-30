import streamlit as st
import s3fs
import dropbox
from dropbox.exceptions import AuthError
import pandas as pd
import pickle


@st.cache_resource
def s3fs_file_system():
    return s3fs.S3FileSystem(anon=False)


@st.cache_resource
def dropbox_connect():
    """Create a connection to Dropbox."""
    try:
        dbx = dropbox.Dropbox(st.secrets["DROPBOX_TOKEN"])
        print("Connected to dropbox")
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def dropbox_list_files(dbx, dropbox_folder_path):
    """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory.
    """
    try:
        files = dbx.files_list_folder(dropbox_folder_path).entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display,
                    'client_modified': file.client_modified,
                    'server_modified': file.server_modified
                }
                files_list.append(metadata)
        df = pd.DataFrame.from_records(files_list)
        return df.sort_values(by='server_modified', ascending=False)
    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))
        return {}


def dropbox_file_exists(dbx, dropbox_folder_path, file):
    df = dropbox_list_files(dbx, dropbox_folder_path)
    return file in df["name"].values


def dropbox_download_file(dbx, dropbox_file_path):
    """Download a file from Dropbox to the local machine."""
    try:
        _, data = dbx.files_download(path=dropbox_file_path)
        data = pickle.loads(data.content)
        return data
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))
        return {}


def dropbox_upload_file(dbx, obj, dropbox_file_path):
    """Upload a file to Dropbox app directory."""
    try:
        meta = dbx.files_upload(pickle.dumps(obj), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))
        return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))
        return []

# dbx = dropbox_connect()
# print(dropbox_file_exists(dbx, "", "Food.pickle"))
# obj = dropbox_download_file(dbx, "/Food.pickle")
# obj["Cia"] = "hello"
# dropbox_upload_file(dbx, obj, "/Food.pickle")
# obj = dropbox_download_file(dbx, "/Food.pickle")
# print(obj)

