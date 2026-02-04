import streamlit as st
from common import my_page_config, thin_gradient_line
from mongodb import get_collection
import pandas as pd
from datetime import datetime
# from cached_data import load_dataframe, load_or_update

def input_page(user_data):

    st.session_state['my_dataframe'] = pd.DataFrame()

    st.markdown('# Requests Input')
    thin_gradient_line()

    col1, col2 = st.columns([1, 3])
    with col1:
        with st.container(border=True):
            st.markdown('#### Requester Details')
            st.markdown(f'{user_data["name"]}')
            st.markdown(f'{user_data["email"]}')
                
        with st.container(border=True):
            st.markdown('#### Client Info')
            
            st.text_input(
                label='Client Name',
                key='client_name')
        
        
            st.text_input(
                label='Agenncy Name',
                key='agency_name')
            
    with col2:
        with st.container(border=True):
            st.markdown('#### Request Info')
            cola, colb, colc = st.columns(3)
            with cola:
                cols = st.columns([1,3])
                with cols[0]:
                    st.markdown('##### Date')
                with cols[1]:
                    st.date_input(
                        label='request_date',
                        label_visibility='collapsed',
                        key='request_date')
            with colb:
                cols = st.columns([1,3])
                with cols[0]:
                    st.markdown('##### Team')
                with cols[1]:
                    st.selectbox(
                        label='ops_team',
                        label_visibility='collapsed',
                        options=['Broadcast', 'Online', 'Print', 'Provincial'],
                        placeholder='Select Team',
                        index=None,
                        key='ops_team')
            
            with colc:
                cols = st.columns([1,3])
                with cols[0]:
                    st.markdown('##### Type')
                with cols[1]:
                    st.selectbox(
                        label='request_type',
                        label_visibility='collapsed',
                        options=['AdHoc', 'Regular', 'TOA'],
                        placeholder='Select Request Type',
                        index=None,
                        key='request_type')
            
            cols = st.columns([1, 11])
            with cols[0]:
                st.markdown('##### URL')
            with cols[1]:
                st.text_area(
                    label='request_url',
                    label_visibility='collapsed',
                    key='request_url')
            
            cols = st.columns([1,11])
            with cols[0]:
                st.markdown('##### Details')
            with cols[1]:
                st.text_area(
                    label='request_details',
                    label_visibility='collapsed',
                    key='request_details')
        
        if st.button(label='Add Entry', width='stretch'):
            
            collection = get_collection('temp')

            _urls = st.session_state['request_url']
            urls = _urls.splitlines()
            
            for _url in urls:
                doc = {
                    'requestor':st.session_state['requester_name'],
                    'client':st.session_state['client_name'],
                    'agency':st.session_state['agency_name'],
                    'request_date':datetime.combine(st.session_state['request_date'],  datetime.min.time()),
                    'team':st.session_state['ops_team'],
                    'request_type':st.session_state['request_type'],
                    'details':st.session_state['request_details'],
                    'url':_url}
                
                if st.session_state['my_dataframe'] == df.empty:
                    df = pd.DataFrame()
                else:
                    df = st.data_editor(st.session_state['my_dataframe'])

                df = pd.concat([df, pd.DataFrame([doc])], ignore_index=True)
                st.session_state['my_dataframe'] = df

                st.dataframe(st.session_state['my_dataframe'])
                
                

    # col1, col2 = st.columns([4,1])
    # with col1:
    #     collection = get_collection('temp')
    #     if collection.count_documents({}) > 0:
    #         docs = list(collection.find({}))
    #         df = pd.DataFrame(docs)
    #         st.dataframe(df)
        




