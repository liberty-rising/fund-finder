import streamlit as st
import requests

API_URL = "http://localhost:8080"  # Update this when deploying

st.title("Grants and Tenders")

# Initialize session state
if "delete_confirmed" not in st.session_state:
    st.session_state.delete_confirmed = False

# Add Update Data section
st.subheader("Update Grants and Tenders Data")
max_items = st.number_input(
    "Max items to fetch (optional)", min_value=1, step=1, value=None
)
update_button = st.button("Fetch Grants and Tenders Data")

if update_button:
    params = {}
    if max_items:
        params["max_items"] = int(max_items)

    response = requests.post(f"{API_URL}/update-data/", params=params)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Failed to start data update. Please try again later.")

# Add reload and delete buttons side by side
col1, col2 = st.columns(2)
with col1:
    if st.button("Reload Grants and Tenders"):
        st.rerun()
with col2:
    if not st.session_state.delete_confirmed:
        if st.button("Delete All Grants and Tenders"):
            st.warning("Are you sure you want to delete all grants and tenders?")
            st.session_state.delete_confirmed = True
            st.rerun()
    else:
        if st.button("Yes, I'm sure"):
            response = requests.delete(f"{API_URL}/grants-tenders/")
            if response.status_code == 200:
                st.success(
                    f"All grants and tenders have been deleted. {response.json()['message']}"
                )
                st.session_state.delete_confirmed = False
                st.rerun()
            else:
                st.error("Failed to delete grants and tenders. Please try again later.")
        if st.button("Cancel"):
            st.session_state.delete_confirmed = False
            st.rerun()

# Fetch and display grants and tenders
response = requests.get(f"{API_URL}/grants-tenders/")
if response.status_code == 200:
    grants_tenders = response.json()
    if not grants_tenders:
        st.info("No grants and tenders available.")
    else:
        for item in grants_tenders:
            st.subheader(item["title"])
            st.write(f"Identifier: {item['identifier']}")
            st.write(f"Status: {item['status']}")
            st.write(f"Fund Type: {item['fund_type']}")
            st.write(f"Start Date: {item['start_date']}")
            st.write(f"Deadline Date: {item['deadline_date']}")
            st.write(f"Description: {item['description']}")
            st.write(f"Keywords: {item['keywords']}")
            st.write(f"Budget: {item['budget']}")
            st.write(f"Call Identifier: {item['call_identifier']}")
            st.write(f"Topic Identifier: {item['topic_identifier']}")
            st.write(f"Topic Conditions: {item['topic_conditions']}")
            st.write(f"Links: {item['links']}")
            st.write("---")
else:
    st.error("Failed to fetch grants and tenders data.")
