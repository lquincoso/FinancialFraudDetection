import streamlit as st
import requests
import datetime
import json
import re
import pandas as pd
import os
#from ..backend.API import main


# Set up title
st.title("Financial Fraud Detection System")

# Add interface selector
interface_option = st.radio(
    "Select Interface",
    ('Transaction Form', 'Transaction Viewer')
)

# If the user selects "Transaction Form"
if interface_option == 'Transaction Form':
    # Transaction Form Interface
    st.header("Enter transaction details")

    randomDigits = r"^C\d{5,14}$"

    # Input fields for the form
    with st.form(key="transaction_form"):
        transaction_date = st.date_input("Transaction date", value=datetime.date.today())
        type = st.selectbox("Transaction type", [" --SELECT A TYPE-- ", "CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"])
        amount = st.number_input("Transaction amount", min_value=0.0, step=0.01)
        oldbalanceOrg = st.number_input("Initial balance", min_value=0.0, step=0.01)
        newbalanceOrig = st.number_input("New balance", min_value=0.0, step=0.01)
        oldbalanceDest = st.number_input("Recipient's Initial balance", min_value=0.0, step=0.01)
        newbalanceDest = st.number_input("Recipient's new balance", min_value=0.0, step=0.01)
        nameOrig = st.text_input("Initiator Name")  # must be C and 5 unique numbers
        nameDest = st.text_input("Recipient Name")  # must be C and 5 random numbers
        submit = st.form_submit_button("Submit")

    # The submit button is where the JSON file gets sent to the API and the dashboard outputs the user results
    if submit:
        if (amount >= 0 and oldbalanceOrg >= 0 and newbalanceOrig >= 0 and oldbalanceDest >= 0 and newbalanceDest >= 0
            and nameOrig and nameDest and re.match(randomDigits, nameOrig)
            and re.match(randomDigits, nameDest) and type != " --SELECT A TYPE-- "):
            
            # The JSON object that will be sent to the database
            new_transaction = {
            "nameOrig": nameOrig,
            #"steps": steps,
            "type": type,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "nameDest": nameDest,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest,
            #"isfraud": isfraud,
            #"isflaggedFraud": isflaggedFraud
            }
            url = 'http://10.108.94.53:5000/api/transaction'
            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.post(url, headers=headers, data=json.dumps(new_transaction))

                # Check the response
                if response.status_code == 200 or response.status_code == 201:
                    st.success('Data sent successfully!')
                else:
                    st.error(f"Failed to send data. Status code: {response.status_code}")
                    st.error(f"Response text: {response.text}")  # This will output the details of the error code 

            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {str(e)}")
            
            #json_data = json.dumps(new_transaction, indent=4)
            st.header("Submitted Transaction in JSON Format")
            st.json(new_transaction)

            st.success(f"Transaction Submitted Successfully!")
            st.write(f"**Date:** {transaction_date}")
            st.write(f"**Transaction Type:** {type}")
            st.write(f"**Transaction amount:** ${amount:.2f}")
            st.write(f"**Initial balance:** ${oldbalanceOrg:.2f}")
            st.write(f"**New balance:** ${newbalanceOrig:.2f}")
            st.write(f"**Recipient's Initial balance:** ${oldbalanceDest:.2f}")
            st.write(f"**Recipient's new balance:** ${newbalanceDest:.2f}")
            st.write(f"**Fraud status:** ${{Insert method}}")
            
        elif (amount >= 0 and oldbalanceOrg >= 0 and newbalanceOrig >= 0 
              and oldbalanceDest >= 0 and newbalanceDest >= 0 and type == " --SELECT A TYPE-- "):
            st.error("Please select a transaction type")      
        else:
            st.error("Please fill in all fields with the appropriate values.")

# If the user selects "Transaction Viewer"
elif interface_option == 'Transaction Viewer':
    # Transaction Viewer Interface
    st.header("Transaction Viewer")

    # API endpoint
    API_URL = "http://10.108.94.53:5000/api/transactions"  # Update with your Flask server URL
    TRANSACTIONS_PER_PAGE = 10

    # Initialize session state for page number if not already present
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

    # Function to increment the page number
    def next_page():
        st.session_state.page_number += 1

    # Function to decrement the page number, ensuring it doesn't go below 1
    def previous_page():
        if st.session_state.page_number > 1:
            st.session_state.page_number -= 1

    # Fetch transactions for the selected page
    def fetch_transactions(page_number):
        params = {'pageNum': page_number}
        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()  # Raise error for bad HTTP status
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code in [400, 404]:
                st.warning("Invalid page number or page not found. Resetting to page 1.")
                st.session_state.page_number = 1
            else:
                st.error(f"Error fetching transactions: {e}")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching transactions: {e}")
            return None

    # Display transactions in a table
    transactions = fetch_transactions(st.session_state.page_number)

    if transactions:
        st.header(f"Transactions - Page {st.session_state.page_number}")

        df = pd.DataFrame(transactions)

        # Adjust the index to show the overall position of each transaction
        start_index = (st.session_state.page_number - 1) * TRANSACTIONS_PER_PAGE
        df.index = range(start_index + 1, start_index + len(df) + 1)

        # Convert Fraudulent and Flagged for Fraud columns to "Yes" or "No"
        df['isfraud'] = df['isfraud'].apply(lambda x: 'Yes' if x == 1 else 'No')
        df['isflaggedFraud'] = df['isflaggedFraud'].apply(lambda x: 'Yes' if x == 1 else 'No')

        # Rename columns
        df = df.rename(columns={
            'nameOrig': 'Sender Name',
            'nameDest': 'Receiver Name',
            'oldbalanceOrg': 'Sender Initial Balance',
            'newbalanceOrig': 'Sender New Balance',
            'oldbalanceDest': 'Receiver Initial Balance',
            'newbalanceDest': 'Receiver New Balance',
            'isfraud': 'Fraudulent',
            'isflaggedFraud': 'Flagged for Fraud'
        })

        # Reorder columns to move Fraudulent and Flagged for Fraud to the right
        cols = [col for col in df.columns if col not in ['Fraudulent', 'Flagged for Fraud']]
        df = df[cols + ['Fraudulent', 'Flagged for Fraud']]

        # Function to highlight the entire row based on Fraudulent and Flagged for Fraud columns
        def highlight_row(row):
            if row['Fraudulent'] == 'Yes':
                return ['background-color: rgba(255, 0, 0, 0.3)'] * len(row)
            elif row['Flagged for Fraud'] == 'Yes':
                return ['background-color: rgba(255, 255, 0, 0.3)'] * len(row)
            else:
                return [''] * len(row)

        # Apply row-level highlighting
        styled_df = df.style.apply(highlight_row, axis=1)

        # Display styled DataFrame
        st.dataframe(styled_df)

        has_next_page = len(transactions) == TRANSACTIONS_PER_PAGE

        col1, col2 = st.columns([1, 1])

        with col1:
            st.button("Previous Page", on_click=previous_page, disabled=(st.session_state.page_number == 1))

        with col2:
            st.button("Next Page", on_click=next_page, disabled=not has_next_page)

    else:
        st.write("No transactions available on this page.")
