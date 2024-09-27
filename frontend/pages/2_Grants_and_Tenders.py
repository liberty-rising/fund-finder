import streamlit as st
import requests

API_URL = "http://localhost:8080"  # Update this when deploying

st.title("Grants and Tenders")

# Add Update Data button
if st.button("Update Grants and Tenders Data"):
    response = requests.post(f"{API_URL}/update-data/")
    if response.status_code == 200:
        st.success("Data update started successfully!")
    else:
        st.error("Failed to start data update. Please try again later.")

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
