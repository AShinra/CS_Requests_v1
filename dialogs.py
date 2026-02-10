import time
import streamlit as st
from argon2 import PasswordHasher
from mongodb import get_collection


@st.dialog(title="Attachment")
def dialog_attachment():
    st.markdown('#### Add Attachment')
    st.file_uploader(label='Upload your file here', key='attachment_file')
    if st.button('Attach File'):
        with st.spinner('Attaching file...'):
            time.sleep(2)
        
        return st.session_state['attachment_file']


@st.dialog(title="Ticket Request Sent")
def dialog_ticket_request(ticket_id, user_email):
    st.markdown(f'#### Ticket Request Sent: {ticket_id}')
    st.markdown(f'An email with the details of your ticket has been sent to **{user_email}**.')
    with st.spinner('Closing.....'):
        time.sleep(2)
        st.rerun()

@st.dialog(title="Password Reset")
def dialog_password_reset(user_data):

    ph = PasswordHasher()
    st.text_input('Enter your old password', key='old_password', type='password')
    
    # verify old password
    if st.session_state.get('old_password'):
        try:
            ph.verify(hash=user_data['password_hash'], password=st.session_state.get('old_password'))
        except:
            st.error('Old password is incorrect.')
            return

    st.text_input('Enter your new password', key='new_password', type='password')
    st.text_input('Confirm new password', key='confirm_password', type='password')

    # create new and confirm password
    if st.session_state.get('new_password') and st.session_state.get('confirm_password'):
        if st.session_state.get('new_password') != st.session_state.get('confirm_password'):
            st.error('New password and confirmation do not match.')
    
    if st.button('Change Password'):
        with st.spinner('Changing password...'):
            time.sleep(2)
            new_password_hash = ph.hash(st.session_state.get('new_password'))
            users_col = get_collection('users')
            users_col.update_one({'name': user_data['name']}, {'$set': {'password_hash': new_password_hash}})
        
        st.success('Password changed successfully.')
        time.sleep(2)
        st.rerun()

    