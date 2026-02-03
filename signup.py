import streamlit as st
from common import password_randomizer, send_test_email

@st.dialog(title="Sign Up")
def dialog_signup():

    # *----------Name-----------*
    cols = st.columns([1,3])
    with cols[0]:
        st.markdown('## Name')
    with cols[1]:
        st.text_input(
            label='Name',
            label_visibility='collapsed',
            key='user_name')
    
    # *----------email-----------*
    cols = st.columns([1,3])
    with cols[0]:
        st.markdown('## Email')
    with cols[1]:
        st.text_input(
            label='Email',
            label_visibility='collapsed',
            key='user_email')

    # *----------user-----------*
    cols = st.columns([1,3])
    with cols[0]:
        st.markdown('## Username')
    with cols[1]:
        st.text_input(
            label='Username',
            label_visibility='collapsed',
            key='user_username')
    
    if st.session_state['user_name'] and st.session_state['user_email'] and st.session_state['user_name']:
        if st.button(label='Create User', key='user_create_btn', width='stretch'):
            # generate randowm password
            password = password_randomizer()
            username = st.session_state['user_username']
            _name = st.session_state['user_name']

            text_to_insert = f"""Hi {_name},
            
            Welcome! 🎉
            Your account has been successfully created using the username you selected during sign-up. You can now log in and start using all available features.

            Username: {username}
            Password: {password}

            If you didn’t create this account or notice anything unusual, please contact our support team immediately.

            Thanks for signing up—we’re glad to have you with us!

            Best regards,
            The Operations Team""" 

            send_test_email(st.session_state['user_email'], text_to_insert)







def signup_user():
    dialog_signup()