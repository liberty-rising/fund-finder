import streamlit as st
import requests
from streamlit.runtime.state import SessionState

API_URL = "http://localhost:8080"  # Update this when deploying

st.title("Register Your Business")

# Initialize session state
if "registration_success" not in st.session_state:
    st.session_state.registration_success = False

business_name = st.text_input("Business Name")
industry = st.selectbox(
    "Industry", ["Technology", "Healthcare", "Finance", "Education", "Other"]
)
size = st.selectbox("Company Size", ["Small", "Medium", "Large"])
annual_revenue = st.number_input("Annual Revenue", min_value=0.0, format="%.2f")

if st.button("Register"):
    response = requests.post(
        f"{API_URL}/businesses/",
        json={
            "name": business_name,
            "industry": industry,
            "size": size,
            "annual_revenue": annual_revenue,
        },
    )
    if response.status_code == 200:
        st.session_state.registration_success = True
        st.success("Business registered successfully!")
    else:
        st.error("Failed to register business.")

if st.session_state.registration_success:
    if st.button("Return to Home"):
        st.session_state.registration_success = False
        st.switch_page("Home.py")
