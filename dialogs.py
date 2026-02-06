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