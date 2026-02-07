from pymongo import MongoClient
import streamlit as st
import time
import os
import gridfs


@st.cache_resource
def connect_to_client():
    return MongoClient(st.secrets["mongodb"]["uri"])

@st.cache_resource
def connect_to_db():
    client = connect_to_client()
    return client['requestdb']

@st.cache_resource
def connect_to_dbattachment():
    client = connect_to_client()
    return client['attachments']

@st.cache_resource
def get_collection(collection_name):
    my_db = connect_to_db()
    return my_db[collection_name]


def check_email_exists(user_email):
    users_collection = get_collection('users')
    result = users_collection.find_one({'email':user_email})
    if result:
        return True

def create_user(userdata):
    with st.spinner("Creating user in database..."):
        
        users_collection = get_collection('users')
        users_collection.insert_one({
            'name':userdata['name'],
            'username':userdata['username'],
            'email':userdata['email'],
            'password_hash':userdata['password'],  # In production, hash the password
            'rights':'user'})

        time.sleep(10)
        st.rerun()

def save_attachment_to_db(file):
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 1️⃣ File name
    file_name = file.name

    # 2️⃣ File path
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # 3️⃣ Save file to disk
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    # 4️⃣ Save to MongoDB GridFS
    fs = gridfs.GridFS(connect_to_dbattachment())
    with open(file_path, "rb") as f:
        file_id = fs.put(f, filename=file_name)
    
    return file_id