import streamlit as st
from common import my_page_config, thin_gradient_line, send_email
from mongodb import get_collection, save_attachment_to_db
import pandas as pd
from datetime import datetime, time
import time
from dialogs import dialog_ticket_request

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
                
                if st.session_state['request_type'] == 'AAF':
                    st.markdown('##### Attachment')
                    file = st.file_uploader(
                        label='Upload Attachment',
                        label_visibility='collapsed',
                        key='attachment_file')
                else:
                    file = None
                
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
            
            doc = {
                'requestor':user_data["name"],
                'client':st.session_state['client_name'],
                'agency':st.session_state['agency_name'],
                'request_date':datetime.combine(_date,  datetime.min.time()),
                'team':st.session_state['ops_team'],
                'request_type':st.session_state['request_type'],
                'details':st.session_state['request_details'],
                'request_status':'Pending',
                'ticket_id':ticket_id,
                'file_id':str(save_attachment_to_db(file) if file else None)}
                        
            with st.spinner('Adding entry...'):
                collection.insert_one(doc)
                dialog_ticket_request(
                    ticket_id=ticket_id,
                    user_email=user_data["email"])
                    # user_email='jonpuray@gmail.com')
                send_email(
                    recipient_email=user_data["email"],
                    email_subject=f'Ticket Request Created: {ticket_id}',
                    text_to_insert=f"""Hi {user_data['name']},
                    
                    Your ticket request with the ID {ticket_id} has been successfully created. Our team will review the details and get back to you as soon as possible.

                    Here are the details of your request:
                    Client: {st.session_state['client_name']}
                    Agency: {st.session_state['agency_name']}
                    Request Type: {st.session_state['request_type']}
                    Request Details: {st.session_state['request_details']}

                    You can track the status of your ticket using the ticket ID provided above.""")
                    

            
            
  




