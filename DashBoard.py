import streamlit as st
import requests
import datetime
import json
import re
import mysql.connector




st.title("Financial fraud detection")

randomDigits = r"^C\d{5,14}$"


st.header("Enter transaction details")

# Input fields for the form
with st.form(key="transaction_form"):
 transaction_date = st.date_input("Transaction date", value=datetime.date.today())
 type = st.selectbox("Transaction type", [" --SELECT A TYPE-- ", "CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"])
 amount = st.number_input("Transaction amount", min_value=0.0, step=0.01)
 oldbalanceOrg = st.number_input("Initial balance", min_value=0.0, step=0.01)
 newbalanceOrig = st.number_input("New balance", min_value=0.0, step=0.01)
 oldbalanceDest = st.number_input("Recipient's Initial balance", min_value=0.0, step=0.01)
 newbalanceDest = st.number_input("Recipient's new balance", min_value=0.0, step=0.01)
 nameOrig = st.text_input("Initiator Name") # must be c and 5 unique numbers
 nameDest = st.text_input("Recipient Name") # must be c and 5 random numbers
 submit = st.form_submit_button("Submit")


# The submit botton is  where the json files gets sent to the API and the dashboard outputs the user results
if submit:
    if ( amount >= 0 and oldbalanceOrg >= 0 and newbalanceOrig >= 0 and oldbalanceDest >= 0 and newbalanceDest >= 0 
        and nameOrig  and nameDest and re.match(randomDigits, nameOrig) 
        and re.match(randomDigits, nameDest)and type != " --SELECT A TYPE-- "):
        
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
        
        
    elif amount >= 0 and oldbalanceOrg >= 0 and newbalanceOrig >= 0 and oldbalanceDest >= 0 and newbalanceDest >= 0 and type == " --SELECT A TYPE-- ":
             st.error("Please select a transaction type")      
    else:
        st.error("Please fill in all fields with the appropriate values.")


st.title("Web Page Navigation")

# Button that opens an external web page
st.markdown("""
    <a href="https://www.google.com/" target="_blank">
        <button style="background-color:green;color:white;padding:10px;border:none;border-radius:5px;">
            Go to Google.com
        </button>
    </a>
""", unsafe_allow_html=True)