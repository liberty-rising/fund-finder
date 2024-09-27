import streamlit as st
import requests

API_URL = "http://localhost:8080"  # Update this when deploying

st.title("Business Opportunity Matcher")

# Business Registration
st.header("Register Your Business")
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
        st.success("Business registered successfully!")
    else:
        st.error("Failed to register business.")

# Opportunity Matching
st.header("Find Matching Opportunities")

# Fetch the list of businesses
response = requests.get(f"{API_URL}/businesses/")
if response.status_code == 200:
    businesses = response.json()
    business_options = [f"{b['id']} - {b['name']}" for b in businesses]
    selected_business = st.selectbox("Select your business", business_options)
    business_id = int(selected_business.split(" - ")[0])
else:
    st.error("Failed to fetch businesses.")
    business_id = None

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

st.header("Update Grants and Tenders Data")
if st.button("Update Data"):
    response = requests.post(f"{API_URL}/update-data/")
    if response.status_code == 200:
        st.success("Data update started successfully!")
    else:
        st.error("Failed to start data update. Please try again later.")

# Display Grants and Tenders
st.header("Grants and Tenders")

# Add a reload button
if st.button("Reload Grants and Tenders"):
    st.rerun()

response = requests.get(f"{API_URL}/grants-tenders/")
if response.status_code == 200:
    grants_tenders = response.json()
    for item in grants_tenders:
        st.subheader(item["title"])
        st.write(f"Identifier: {item['identifier']}")
        st.write(f"Status: {item['status']}")
        st.write(f"Publication Date: {item['publication_date']}")
        st.write(f"Deadline Date: {item['deadline_date']}")
        st.write(f"Description: {item['description']}")
        st.write("---")
else:
    st.error("Failed to fetch grants and tenders data.")
