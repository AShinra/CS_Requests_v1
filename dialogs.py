import time
import streamlit as st



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