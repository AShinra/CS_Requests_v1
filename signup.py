import streamlit as st
from common import password_randomizer, send_email, is_valid_email
from mongodb import create_user, check_email_exists
from argon2 import PasswordHasher
import datetime

@st.dialog(title="Sign Up")
def dialog_signup():

    with st.container(border=True):  
        # *----------Name-----------*
        cols = st.columns([2,5])
        with cols[0]:
            st.markdown('### Name:red[*]')
        with cols[1]:
            st.text_input(
                label='Name',
                label_visibility='collapsed',
                key='user_name')
        
        # *----------user-----------*
        cols = st.columns([2,5])
        with cols[0]:
            st.markdown('### Username:red[*]')
        with cols[1]:
            st.text_input(
                label='Username',
                label_visibility='collapsed',
                key='user_username')
            
        # *----------email-----------*
        cols = st.columns([2,5])
        with cols[0]:
            st.markdown('### Email:red[*]')
        with cols[1]:
            st.text_input(
                label='Email',
                label_visibility='collapsed',
                key='user_email')

        
    if st.session_state['user_name'] and st.session_state['user_email'] and st.session_state['user_username']:
        if check_email_exists(st.session_state['user_email'])==True:
            st.error("Email already exists. Please use a different email.")
        else:
            if is_valid_email(st.session_state['user_email'])==True:
                if st.button(label='Create User', key='user_create_btn', width='stretch'):
                    # generate randowm password
                    password = password_randomizer()
                    username = st.session_state['user_username']
                    _name = st.session_state['user_name']
                    _subject = "Welcome! Your Account Has Been Created"

                    text_to_insert = f"""Hi {_name},
                    
                    Welcome! 🎉
                    Your account has been successfully created using the username you selected during sign-up. You can now log in and start using all available features.

                    Here are your account details:
                    Username: {username}
                    Password: {password}
                    https://requests-v1.streamlit.app/

                    If you didn’t create this account or notice anything unusual, please contact our support team immediately.

                    Thanks for signing up—we’re glad to have you with us!

                    Best regards,
                    The Operations Team""" 

                    send_email(
                        recipient_email=st.session_state['user_email'],
                        email_subject=_subject,
                        text_to_insert=text_to_insert)
                    
                    ph = PasswordHasher()
                    hashed_password = ph.hash(password)
                    
                    create_user({
                        "name": st.session_state['user_name'],
                        "username": st.session_state['user_username'],
                        "email": st.session_state['user_email'],
                        "password": hashed_password,
                        "rights": "user",
                        "joined": datetime.now().date(),
                        "phone": None,
                        "location": None})

            else:
                st.error("Please enter a valid email address.")
