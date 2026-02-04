import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import random
import string
import time
from email_validator import validate_email, EmailNotValidError
from mongodb import create_user

def my_page_config():
    '''
    Contains global formatting for text and spacing
    '''

    st.set_page_config(
        page_title='Operations Request Module',
        page_icon='🏬',
        layout='wide'
        )
    
       
    st.markdown(
    """
    <style>
    
    .block-container {
        padding-top: 0rem; /* Adjust this value as needed (e.g., 0rem for minimal padding) */
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }   

    </style>
    """,
    unsafe_allow_html=True
    )

    
    st.markdown("""
    <style>

    div[data-baseweb="tab-list"] {
    display: flex;
    gap: 0;}

    button[data-baseweb="tab"] {
        flex: 1;
        font-size: 16px;
        padding: 10px 16px;
        text-align: center;
        border: 3px solid transparent;   /* 👈 inactive border color */
        color: #;}

    /* Hover */
    button[data-baseweb="tab"]:hover {
        border-color: #000000;
        border-radius: 15px 15px 0 0;
        color: #ffffff;
        background-color: #423738;}

    /* Active tab */
    button[data-baseweb="tab"][aria-selected="true"] {
        border-color: #dfb011;      /* 👈 active border color */
        color: #ffffff;
        font-weight: 600;
        border-radius: 15px 15px 0 0;
        background-color: #423738;}
    </style>
    """, unsafe_allow_html=True)
    

def thin_gradient_line():
    st.markdown("<hr style='border: 0; height: 5px; padding: 0; margin: 0; background: linear-gradient(to right, #d0c09e, #f4b315);'/>", unsafe_allow_html=True)

def access_gsheet():
    # access public google sheet
    sheet_id = "1KqXTe99Vb5SR_1JTf-F8V1qPfhWmffPO"
    gid = "807112605"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    # convert to dataframe
    df = pd.read_csv(url)

    # drop blank rows
    df = df.dropna(how="all")

    # rename column
    df.rename(columns={
        df.columns[0]:'Request_Date',
        df.columns[1]:'Name'
    }, inplace=True)

    return df
    

def send_test_email(recipient_email, text_to_insert):
    # Email details
    sender_email = st.secrets['my_email']['email']
    receiver_email = recipient_email
    password = st.secrets['my_email']['pass']  # not your normal password

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Welcome! Your Account Has Been Created"
    msg.set_content(text_to_insert)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)

    with st.spinner("Sending email..."):
        time.sleep(2)  # Simulate delay

    st.success("Successfully sent email to {}".format(recipient_email))
    

def password_randomizer():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    return password

def is_valid_email(email):
    try:
        # Validate and get info
        valid = validate_email(email)
        email = valid.email  # normalized email
        return True
    except EmailNotValidError as e:
        print(str(e))
        return False







