# Shellhacks - Team CafecitoFIU105 Fall 2024
### ====Florida International Universty=====

## Project Title: Machine Learning Fraud Detection 

### Team Members:
	- Lorena A. Quincoso Lugones
	- Ibsen Martinez
	- Fabio Hernandez Rubio
	- Jesus Valdes


## Code Directory Structure:
The folder structure goes as follows:
```css
FinancialFraudDetection/        	# Root directory of the financial fraud detection project
├── backend/                    	# Directory for the backend logic and API for the project
│   ├── API/                    	# Directory for API-related files and model handling
│       ├── model/              	# Contains the trained fraud detection model and associated files
|           ├── Fraud_Model.ipynb   	# Jupyter notebook used to train and analyze the fraud detection model
|           ├── feat_columns.pkl    	# Pickle file storing the feature columns used for training
│           ├── fraud_model.pkl     	# Pickle file storing the trained fraud detection model
|           ├── le_nameDest.pkl     	# Pickle file storing the label encoder for destination names
│           └── le_nameOrig.pkl     	# Pickle file storing the label encoder for origin names
|       ├── db.py                  	# Script for managing database connections and functions
|       ├── main.py                	# Main script to run the backend API server (routes with methods and helper methods)
|       ├── predictions.py         	# Script handling model predictions methods
│   ├── SQL/                       	# Contains SQL scripts for database setup
│       └── TransactionsTable.sql  	# SQL file to create the structure of the transactions table
|   ├── requirements.txt           	# List of dependencies required for the backend
├── frontend/                      	# Contains files related to the frontend UI
│   └── dashboard.py               	# Python file for creating the interface using strimlit
├── .gitignore                     	# Specifies files to be ignored by Git version control
└── README.md                      	# Documentation providing an overview and instructions for the project
```


### User Guide:

1. Start MySQL Server and run Backend/API/SQL/TransactionsTable.sql
2. Install python dependencies (pip install) within the Backend/API/requirements.txt
3. Run API file in the Backend/API/main.py
4. Run interface file in the frontend/dashboard.py


### Model Instructions:

3.1: Run the Jupyter Notebook under 'Fraud_Model.ipynb' folder in order to see the training/testing model on the dataset.
3.2: Access if possible to the Command Prompt (Commander from Anaconda Navigator is recommended), and type: 'pip install streamlit-folium' if you don't have the package installed already on your system.
3.3: Through the same Prompt, 'cd' to the downloaded folder.
3.4: Ensure the dependencies are installed by typing on the Prompt: 'pip install -r requirements.txt'.


================================================================================================

### Technologies:
ML Model: Jupyter Notebook, Random Forest Classifier, Anaconda
API: Flask
Database: MySQL
Frontend: Strimlit

