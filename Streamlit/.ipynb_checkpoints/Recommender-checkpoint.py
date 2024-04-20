#import packages
import streamlit as st
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics.pairwise import cosine_similarity

from POI_ratings_recommender import main_recommender,process_output,load_users # this .py file has the logic for the recommendations

#Add sidebar to the app
st.sidebar.markdown("### What's Next to do ")
st.sidebar.markdown("Welcome to planning an itenerary. This app is built using Streamlit and uses data sourced from Ticket Master, Yelp and FourSquare. I hope you enjoy!")

#Add title and subtitle to the main interface of the app
st.title("Make planning easier !! ")

# to get user and city information
POI_user,TM_user =load_users()
# Concatenate user_name columns and get unique user names
user_names = pd.concat([POI_user, TM_user])['user_name'].dropna().unique()
city_name=pd.concat([POI_user['City'], TM_user['city']]).dropna().unique()
sorted_cities = sorted(city_name)

# Display dropdown menu in Streamlit
selected_user = st.selectbox("User Login ", user_names)
selected_city= st.selectbox("Select your destination in Canada ", sorted_cities)


# Call the function main_recommender to get user_data according to the selection
similar_users_df,suggestions= main_recommender(selected_user,selected_city)

#import the process_output function to get information matching the filters provided and the similar users
restaurants,Events,suggested_restaurant,suggested_POI,suggested_events = process_output(similar_users_df,suggestions,selected_city)


# Display recommendations
st.write("Recommendations for : ",selected_user)
if len(restaurants)>0:
    df1=pd.DataFrame(restaurants)
    st.write("Restaurants to visit : ")
    st.write(df1.head())
else:
    st.write("No restaurant recommendations available.")


if len(Events)>0:
    df2=pd.DataFrame(Events)
    st.write("Events in the area :")
    st.write(df2.head())
else:
    st.write("No Events.")

# if len(POI)>0:
#     df3=pd.DataFrame(POI)
#     st.write("Places to visit :")
#     st.write(df3.head())
# else:
#     st.write("No recommendations.")

    


