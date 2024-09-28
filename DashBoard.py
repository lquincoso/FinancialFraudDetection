import streamlit as st
import requests
import datetime
import json
import mysql.connector



st.title("Financial fraud detection")


# Create a form for inputting transaction details
st.header("Enter transaction details")

# Input fields for the transaction form
with st.form(key="transaction_form"):
 transaction_date = st.date_input("Transaction date", value=datetime.date.today())
 type = st.selectbox("Transaction type", [" ", "CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"])
 amount = st.number_input("Transaction amount", min_value=0.0, step=0.01)
 oldbalanceOrg = st.number_input("Initial balance", min_value=0.0, step=0.01)
 newbalanceOrig = st.number_input("New balance", min_value=0.0, step=0.01)
 oldbalanceDest = st.number_input("Recipient's Initial balance", min_value=0.0, step=0.01)
 newbalanceDest = st.number_input("Recipient's new balance", min_value=0.0, step=0.01)
 nameOrig = st.text_input("Sender Name")
 nameDest = st.text_input("Receiver Name")
 submit = st.form_submit_button("Submit")


# Button to submit the transaction
if submit:
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
    url = 'http://10.108.94.53:5000/api/transaction'  # Replace with your actual API endpoint
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(new_transaction))

        # Check the response
        if response.status_code == 200:
            st.success('Data sent successfully!')
        else:
            st.error(f"Failed to send data. Status code: {response.status_code}")
            st.error(f"Response text: {response.text}")  # Log the response content for more debugging info

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {str(e)}")
    

    #json_data = json.dumps(new_transaction, indent=4)

    st.header("Submitted Transaction in JSON Format")
    st.json(new_transaction)
    
    if  amount >= 0 and oldbalanceOrg >= 0 and newbalanceOrig >= 0 and oldbalanceDest >= 0 and newbalanceDest >= 0 and type != " ":
        # Display a summary of the transaction
        st.success(f"Transaction Submitted Successfully!")
        st.write(f"**Date:** {transaction_date}")
        st.write(f"**Transaction Type:** {type}")
        st.write(f"**Transaction amount:** ${amount:.2f}")
        st.write(f"**Initial balance:** ${oldbalanceOrg:.2f}")
        st.write(f"**New balance:** ${newbalanceOrig:.2f}")
        st.write(f"**Recipient's Initial balance:** ${oldbalanceDest:.2f}")
        st.write(f"**Recipient's new balance:** ${newbalanceDest:.2f}")
        st.write(f"**Fraud status:** ${{Insert method}}")
        
        # Optionally, add the transaction to a list or a database
        # You could store these details in a database or process further
        # transactions.append({"sender": sender, "receiver": receiver, "amount": amount, "date": transaction_date})
    elif amount >= 0 and oldbalanceOrg >= 0 and newbalanceOrig >= 0 and oldbalanceDest >= 0 and newbalanceDest >= 0 and type == " ":
             st.error("Please select a transaction type")      
    else:
        st.error("Please fill in all fields with the appropriate values.")

