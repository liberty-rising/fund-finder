import streamlit as st
import requests

API_URL = "http://localhost:8080"  # Update this when deploying

st.set_page_config(page_title="Business Opportunity Matcher", page_icon="💼")

# Add a button to register a new business
if st.button("Register a New Business"):
    st.switch_page("pages/1_Register_Business.py")

# Fetch the list of businesses
response = requests.get(f"{API_URL}/businesses/")
if response.status_code == 200:
    businesses = response.json()
    if businesses:
        business_options = [f"{b['id']} - {b['name']}" for b in businesses]
        selected_business = st.selectbox("Select a business", business_options)

        business_id = int(selected_business.split(" - ")[0])

        # Fetch details for the selected business
        response = requests.get(f"{API_URL}/businesses/{business_id}")
        if response.status_code == 200:
            business = response.json()
            st.title(f"{business['name']}")
            st.write(f"Industry: {business['industry']}")
            st.write(f"Size: {business['size']}")
            st.write(f"Annual Revenue: ${business['annual_revenue']:,.2f}")

            # Create two columns for the "Find Matches" and "Delete Business" buttons
            col1, col2 = st.columns([3, 1])

            with col1:
                if st.button("Find Matches"):
                    match_response = requests.post(
                        f"{API_URL}/match/", params={"business_id": business_id}
                    )
                    if match_response.status_code == 200:
                        opportunities = match_response.json()
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

            with col2:
                if st.button("Delete Business", key="delete_business"):
                    delete_response = requests.delete(
                        f"{API_URL}/businesses/{business_id}"
                    )
                    if delete_response.status_code == 200:
                        st.success(f"Business deleted successfully.")
                        st.rerun()  # Rerun the app to refresh the business list
                    else:
                        st.error("Failed to delete the business.")
        else:
            st.error("Failed to fetch business details.")
    else:
        st.info("No businesses registered yet.")
else:
    st.error("Failed to fetch businesses.")
