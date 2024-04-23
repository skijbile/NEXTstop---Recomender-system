#import packages
import streamlit as st
import time
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from POI_ratings_recommender import main_recommender,process_output,load_users,pre_process,get_recommendations # this .py file has the logic for the recommendations


#Add sidebar to the app
st.sidebar.markdown("### NEXTstop ")
st.sidebar.markdown("Welcome to planning an itenerary. This app is built using Streamlit and uses data sourced from Ticket Master, Yelp and FourSquare. I hope you enjoy!")

#Add title and subtitle to the main interface of the app
st.title("Make planning easier !! ")

# Add a placeholder to display a message
placeholder = st.empty()

# Display a message to the user
placeholder.text("Please input values below:")

# to get user and city information
POI_user,TM_user =load_users()
# Concatenate user_name columns and get unique user names
user_names = pd.concat([POI_user, TM_user])['user_name'].dropna().unique()
city_name=pd.concat([POI_user['City'], TM_user['city']]).dropna().unique()
sorted_cities = city_name


# Display dropdown menu in Streamlit
selected_user = st.selectbox("User Login ", user_names)
selected_city= st.selectbox("Select your destination in Canada ",sorted_cities)

# Get the session state object
session_state = st.session_state


# Add a "Proceed" button
proceed = st.button("Next")

# Use st.experimental_rerun() to halt execution until "Proceed" button is clicked
if proceed:
    # Proceed with the rest of your app logic
    placeholder.text("Processing...")
     # Get or calculate recommendations
    recommendations = get_recommendations(selected_user, selected_city, session_state)
    placeholder.text("Processing complete!")
    placeholder.text("Getting recommendations!")

    if recommendations:
            restaurants, Events, POI, suggested_restaurant, suggested_POI, suggested_events = recommendations
# # Call the function main_recommender to get user_data according to the selection
#     similar_users_df,suggestions= main_recommender(selected_user,selected_city)


# #import the process_output function to get information matching the filters provided and the similar users
#     restaurants,Events,POI,suggested_restaurant,suggested_POI,suggested_events = process_output(similar_users_df,suggestions,selected_city,yelp_POI,TM_events,foursq_POI)


    placeholder.text("Printing recommendations!")

# Display recommendations
    st.write("Top Recommendations for : ",selected_user)
    if len(Events)>0:
        df1=pd.DataFrame(Events)
        df1.reset_index(drop=True, inplace=True)  # Reset index
        # Setting index starting from 1
        df1.index = df1.index + 1
        st.write("Events in the area :")
        st.write(df1.head(10))
    else:
        st.write("No Events.")
        df1=pd.DataFrame(suggested_events)
        df1.reset_index(drop=True, inplace=True)
        # Setting index starting from 1
        df1.index = df1.index + 1
        st.write("Other options :")
        st.write(df1.head())
        
    if len(restaurants)>0:
        df2=pd.DataFrame(restaurants)
        df2.reset_index(drop=True, inplace=True)  # Reset index
        # Setting index starting from 1
        df2.index = df2.index + 1
        st.write("Restaurants to visit : ")
        st.write(df2.head(10))
    else:
        st.write("No restaurant recommendations available.")
        df2=pd.DataFrame(suggested_restaurant)
        df2.reset_index(drop=True, inplace=True)  # Reset index
        # Setting index starting from 1
        df2.index = df2.index + 1
        st.write("Other options : ")
        st.write(df2.head())

    if len(POI)>0 :
        df3=pd.DataFrame(POI)
        df3.reset_index(drop=True, inplace=True) # Reset index
        # Setting index starting from 1
        df3.index = df3.index + 1
        st.write("Places to visit :")
        st.write(df3.head(10))
    else:
        if len(suggested_POI)> 0:
            df3=pd.DataFrame(suggested_POI)
            df3.reset_index(drop=True, inplace=True)  # Reset index
            # Setting index starting from 1
            df3.index = df3.index + 1
            st.write("People have also visited :")
            st.write(df3.head())
        else:
            st.write("No recommendations.")



else:
    st.stop()  # Stop execution until the button is clicked
    


