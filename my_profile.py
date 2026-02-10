import streamlit as st
from mongodb import get_collection
from common import thin_gradient_line
from dialogs import dialog_password_reset



def my_profile_page(user_data):

    st.markdown('# My Profile')
    thin_gradient_line()

    
    # Header
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg?semt=ais_hybrid&w=740&q=80", width=300)
    with col2:
        st.subheader(user_data['name'])
        st.caption(user_data['rights'].capitalize())
        st.button("Edit Profile", width=150)
        if st.button("Edit Password", width=150):
            dialog_password_reset(user_data)

    st.markdown("---")

    # Contact Info
    st.subheader("Contact Info")
    st.text(f"Email: {user_data['email']}")
    st.text(f"Phone: {user_data['phone']}")
    st.text(f"Location: {user_data['location']}")
    st.text(f"Joined: {user_data['joined']}")

    
