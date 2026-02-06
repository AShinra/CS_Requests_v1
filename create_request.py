import streamlit as st
from common import my_page_config, thin_gradient_line
from mongodb import get_collection, connect_to_dbattachment
import pandas as pd
from datetime import datetime, time
import time
from dialogs import dialog_attachment
import gridfs
import os
# from cached_data import load_dataframe, load_or_update

def input_page(user_data):

    st.session_state['my_dataframe'] = pd.DataFrame()

    st.markdown('# Requests Input')
    thin_gradient_line()

    col1, col2 = st.columns([1, 3])
    with col1:
        with st.container(border=True):
            st.markdown('#### Requester Details')
            thin_gradient_line()
            cols = st.columns([1,3])
            with cols[0]:
                st.markdown('##### Date')
            with cols[1]:
                _date = datetime.now()
                st.markdown(f'{_date.strftime("%B %d, %Y")}')
            cols = st.columns([1,3])
            with cols[0]:
                st.markdown('##### Name')
            with cols[1]:
                st.markdown(f'{user_data["name"]}')
            cols = st.columns([1,3])
            with cols[0]:
                st.markdown('##### Email')
            with cols[1]:
                st.markdown(f'{user_data["email"]}')
                
        with st.container(border=True):
            st.markdown('#### Assigned to')
            thin_gradient_line()
            cols = st.columns([1,3])
            with cols[0]:
                st.markdown('##### Team')
            with cols[1]:
                st.selectbox(
                    label='ops_team',
                    label_visibility='collapsed',
                    options=['Broadcast', 'Online', 'Operations Manager', 'Print', 'Provincial'],
                    placeholder='Select Team',
                    index=None,
                    key='ops_team')
            
            
            
    with col2:
        with st.container(border=True):
            st.markdown('#### Request Details')
            thin_gradient_line()
            cola, colb = st.columns([1,2])
            
            with cola:
                cols = st.columns([1,3])
                with cols[0]:
                    st.markdown('##### Type')
                with cols[1]:
                    st.selectbox(
                        label='request_type',
                        label_visibility='collapsed',
                        options=['AAF', 'Validation', 'Others'],
                        placeholder='Select Request Type',
                        index=None,
                        key='request_type')
                
                cols = st.columns([1,3])
                with cols[0]:
                    st.markdown('##### Agency')
                with cols[1]:
                    st.text_input(
                        label='Agency',
                        label_visibility='collapsed',
                        placeholder='Enter Agency Name',
                        key='agency_name')
                
                cols = st.columns([1,3])
                with cols[0]:
                    st.markdown('##### Client')
                with cols[1]:
                    st.text_input(
                        label='Client',
                        label_visibility='collapsed',
                        placeholder='Enter Client Name',
                        key='client_name')
                
                st.markdown('##### Attachment')
                file = st.file_uploader(
                    label='Upload Attachment',
                    label_visibility='collapsed',
                    key='attachment_file')
                
                
                        
                    
                    
            
            with colb:           
                st.text_area(
                    label='request_details',
                    label_visibility='collapsed',
                    placeholder='Enter request details here',
                    height=500,
                    key='request_details')
        
        if st.button(label='Add Entry', width='stretch'):
            
            year_now = datetime.now().year
            collection_len = get_collection('temp').count_documents({})
            ticket_id = f'CS-{year_now}-{str(collection_len + 1).zfill(5)}'
            collection = get_collection('temp')
            
            UPLOAD_DIR = "uploads"
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            if file is not None:
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

            doc = {
                'requestor':user_data["name"],
                'client':st.session_state['client_name'],
                'agency':st.session_state['agency_name'],
                'request_date':datetime.combine(_date,  datetime.min.time()),
                'team':st.session_state['ops_team'],
                'request_type':st.session_state['request_type'],
                'details':st.session_state['request_details'],
                # 'attachment':st.session_state['attachment_file'],
                'request_status':'Pending',
                'ticket_id':ticket_id,
                'file_id':str(file_id)}
                        
            with st.spinner('Adding entry...'):
                collection.insert_one(doc)
            
            
                
                
                
                

    # col1, col2 = st.columns([4,1])
    # with col1:
    #     collection = get_collection('temp')
    #     if collection.count_documents({}) > 0:
    #         docs = list(collection.find({}))
    #         df = pd.DataFrame(docs)
    #         st.dataframe(df)
        




