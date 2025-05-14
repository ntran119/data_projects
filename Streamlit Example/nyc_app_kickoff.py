### KICKOFF - CODING AN APP IN STREAMLIT

### import libraries
import pandas as pd
import streamlit as st
import joblib

st.write('Streamlit is an open-source app framework for Machine Learning and Data Science teams. For the docs, please click [here](https://docs.streamlit.io/en/stable/api.html). \
    This is is just a very small window into its capabilities.')


#######################################################################################################################################
### LAUNCHING THE APP ON THE LOCAL MACHINE
### 1. Save your *.py file (the file and the dataset should be in the same folder)
### 2. Open git bash (Windows) or Terminal (MAC) and navigate (cd) to the folder containing the *.py and *.csv files
### 3. Execute... streamlit run <name_of_file.py>
### 4. The app will launch in your browser. A 'Rerun' button will appear every time you SAVE an update in the *.py file


#######################################################################################################################################
### Create a title

# Press R in the app to refresh after changing the code and saving here

#######################################################################################################################################
### DATA LOADING

### A. define function to load data




#######################################################################################################################################
### STATION MAP







#######################################################################################################################################
### DATA ANALYSIS & VISUALIZATION

### B. Add filter on side bar after initial bar chart constructed


### A. Add a bar chart of usage per hour


#######################################################################################################################################
### MODEL INFERENCE

# A. Load the model using joblib



# B. Set up input field



# C. Use the model to predict sentiment & write result




#######################################################################################################################################
### STREMLIT ADVANTAGES AND DISADVANTAGES
    
#st.subheader("Streamlit Advantages and Disadvantages")
#st.write('**Advantages**')
#st.write(' - Easy, Intuitive, Pythonic')
#st.write(' - Free!')
#st.write(' - Requires no knowledge of front end languages')
#st.write('**Disadvantages**')
#st.write(' - Apps all look the same')
#st.write(' - Not very customizable')
#st.write(' - A little slow. Not good for MLOps, therefore not scalable')


