import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Update this when deploying

st.title("Business Opportunity Matcher")

# Business Registration
st.header("Register Your Business")
business_name = st.text_input("Business Name")
industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Education", "Other"])
size = st.selectbox("Company Size", ["Small", "Medium", "Large"])
annual_revenue = st.number_input("Annual Revenue", min_value=0.0, format="%.2f")

if st.button("Register"):
    response = requests.post(f"{API_URL}/businesses/", json={
        "name": business_name,
        "industry": industry,
        "size": size,
        "annual_revenue": annual_revenue
    })
    if response.status_code == 200:
        st.success("Business registered successfully!")
    else:
        st.error("Failed to register business.")

# Opportunity Matching
st.header("Find Matching Opportunities")
business_id = st.number_input("Enter your Business ID", min_value=1, step=1)

if st.button("Find Matches"):
    response = requests.post(f"{API_URL}/match/", params={"business_id": business_id})
    if response.status_code == 200:
        opportunities = response.json()
        if opportunities:
            for opp in opportunities:
                st.subheader(opp["title"])
                st.write(f"Type: {opp['type']}")
                st.write(f"Amount: ${opp['amount']:.2f}")
                st.write(f"Description: {opp['description']}")
                st.write("---")
        else:
            st.info("No matching opportunities found.")
    else:
        st.error("Failed to fetch matching opportunities.")