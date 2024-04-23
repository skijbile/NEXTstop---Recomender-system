#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# define function to import user data 
def load_users():
    POI_user=pd.read_csv("Data/After EDA/POI_Ratings.csv")
    TM_user=pd.read_csv("Data/After EDA/Venue_Reviews.csv")
    
    return POI_user,TM_user
    

def main_recommender( user_name,user_city ):
    # import data for the recommender using function
    venue_ratings,POI_ratings=load_users()
    venue_ratings.rename(columns={'Event_type': 'Category'}, inplace=True)
    

    # merge data
    ratings_df=pd.concat([venue_ratings,POI_ratings])
    ratings_df.drop_duplicates()#.shape

    # drop columns not required
    columns_to_drop=['Address_y','latitude','longitude']
    ratings_df.drop(columns=columns_to_drop,axis=1,inplace=True)

    ratings_df['city'].fillna(ratings_df['City'],inplace=True)
    ratings_df=ratings_df.drop_duplicates()
    ratings_df.drop(['City'],inplace=True,axis=1)

    #  change the NaN ratings to -1 to indicate that they are missing, and convert the user_id,user_name to string "Not available" so that there are no NaN values in the matrix 

    ratings_df['ratings']=ratings_df['ratings'].replace(np.nan,-1)
    ratings_df[['user_id','user_name']]=ratings_df[['user_id','user_name']].replace(np.nan,"Ratings not available")

# Build Recommender

    # Create the pivot table
    recommender_matrix = ratings_df.pivot_table(index='user_id', columns='Category', values='ratings')
    user_city= user_city # filter for the ratings to only show those options
    user= user_name     # select user login
    matched_user=ratings_df[ratings_df['user_name']==user]
    matched_id=matched_user['user_id'].unique()

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(recommender_matrix.fillna(0))

    # Convert similarity matrix into DataFrame
    similarity_df = pd.DataFrame(similarity_matrix, index=recommender_matrix.index, columns=recommender_matrix.index)

    # Find users similar to selected user
    similarities_to_given_user = similarity_df.loc[matched_id[0]].sort_values(ascending=False)

    # Return a df of similar users
    similar_users_data = []

    # Iterate over the index of similarities_to_given_user
    for user_id in similarities_to_given_user[similarities_to_given_user != 0].index:
        # Filter ratings_df for rows with matching user IDs
        similar_user_data = ratings_df[ratings_df['user_id'] == user_id]
    
        # Append the filtered data to similar_users_data list
        similar_users_data.append(similar_user_data)

    # Concatenate the filtered data into a single DataFrame
    similar_users_df = pd.concat(similar_users_data)


    # Return a df of venues not similar but as suggestions
    dis_similar = []

    # Iterate over the index of similarities_to_given_user
    for user_id in similarities_to_given_user[similarities_to_given_user == 0].index:
        # Filter ratings_df for rows with matching user IDs
        dis_similar_data = ratings_df[ratings_df['user_id'] == user_id]
    
        # Append the filtered data to similar_users_data list
        dis_similar.append(dis_similar_data)

    # Concatenate the filtered data into a single DataFrame
    suggestions = pd.concat(dis_similar)

    return similar_users_df, suggestions

def pre_process():
# Pre=processing 
    # import all required csv's for output
    yelp_POI = pd.read_csv("Data/After EDA/Yelp_Data_1EDA.csv")
    TM_events = pd.read_csv('Data/After EDA/TM_data_EDA.csv')
    foursq_POI = pd.read_csv("Data/After EDA/FourSq_data_EDA.csv")
    

    # fix the data frames for the output
    # by dropping columns
    # by re-arranging the columns
    # by renaming columns names

    columns_to_drop1=["Business ID","State_x","Latitude","Longitude","latitude","longitude","Address_y"]
    yelp_POI.drop(columns=columns_to_drop1,inplace=True,axis=1)
    desired_columns_1=['Name', 'Category','Ratings', 'Pricing','Address_x' , 'City','State_y','Distance_From_Venue',
       'Venue']
    yelp_POI=yelp_POI[desired_columns_1]
    column_mapping={'Address_x' :'Address',
                'State_y':'State'}
    yelp_POI.rename(columns=column_mapping,inplace=True)
                
    columns_to_drop_2=["Latitude","Longitude"]
    TM_events.drop(columns=columns_to_drop_2,inplace=True,axis=1)
    desired_columns_2=['Event_name', 'Event_type', 'Event_dates', 'Event_start_times','Last_Purchase_Date','Venues','Age_restrictions','Ticket_limits',
       'Parking', 'Accesibility',
       'Event_time_zone',  'City', 'States', 'Address','Additional_info']
    TM_events=TM_events[desired_columns_2]

    # Reset the index of the DataFrame (if needed)
    #foursq_POI.reset_index(drop=True, inplace=True)
    desired_columns_3=["POI","Category","Address","City","State","Distance From Venue","Venue"]
    foursq_POI = foursq_POI[ desired_columns_3]

    return yelp_POI,TM_events,foursq_POI

def process_output(similar_users_df, suggestions,user_city,yelp_POI,TM_events,foursq_POI):
# Process the users data from the main_recommender
    # Calculate average ratings by venue for dis-similar items

    average_ratings_by_venue = suggestions.groupby('venue')['ratings'].mean().reset_index()
    average_ratings_by_venue.columns = ['venue', 'average_ratings']  # Rename columns for clarity
    average_ratings_by_venue['average_ratings'] = average_ratings_by_venue['average_ratings'].round(1) # round the value to 1 decimal

    # Merge average ratings back into the original DataFrame
    suggestions_with_avg_ratings = pd.merge(suggestions, average_ratings_by_venue, on='venue', how='left')
    sorted_suggestions=suggestions_with_avg_ratings.sort_values(by='average_ratings', ascending=False)

    similar_users_df=similar_users_df[similar_users_df['city']==user_city]

    # we use the sorted suggestions to view places with higher ratings 
    sorted_suggestions=sorted_suggestions[sorted_suggestions['city']==user_city]


# Recommender output

    restaurants=[]
    Events=[]
    POI=[]

    for item in similar_users_df['venue'].unique():
        for index2,row2 in TM_events.iterrows() :
            if item in row2['Venues'] and row2['City']==user_city:
                Events.append(row2)
                break
        for index,row in yelp_POI.iterrows():
             if isinstance(row['Name'], str) and row['City']==user_city and item in row['Name'] :
                restaurants.append(row)
                break
        for index1, row1 in foursq_POI.iterrows():
            poi_value = row1['POI']
            if isinstance(poi_value, str) and row1['City']==user_city and item in poi_value :
                POI.append(row1)
                break  # Stop searching after finding a match

    # optional places

    suggested_restaurant=[]
    suggested_POI=[]
    suggested_events=[]

    for items in sorted_suggestions['venue'].unique():
        for index,row in yelp_POI.iterrows():
            if isinstance(row['Name'], str) and row['City']==user_city and items in row['Name'] :
                suggested_restaurant.append(row)
                break
        for index1, row1 in foursq_POI.iterrows():
            poi_value = row1['POI']
            if isinstance(poi_value, str) and items in poi_value and row1['City']==user_city:
                suggested_POI.append(row1)
                break  # Stop searching after finding a match

        for index2,row2 in TM_events.iterrows() :
            if items in row2['Venues'] and row2['City']==user_city:
                suggested_events.append(row2)
                break
                
    return restaurants,Events,POI,suggested_restaurant,suggested_POI,suggested_events

def print_recommendations(selected_user, selected_city, Events, suggested_events, restaurants, suggested_restaurant, POI, suggested_POI):
    recommendation = {
        'selected_user': selected_user,
        'selected_city': selected_city,
    }

    if len(Events) > 0:
        df1 = pd.DataFrame(Events)
        df1.reset_index(drop=True, inplace=True)
        df1.index = df1.index + 1
        recommendation['events'] = df1.head(10)
    else:
        df1 = pd.DataFrame(suggested_events)
        df1.reset_index(drop=True, inplace=True)
        df1.index = df1.index + 1
        recommendation['events'] = df1.head()

    if len(restaurants) > 0:
        df2 = pd.DataFrame(restaurants)
        df2.reset_index(drop=True, inplace=True)
        df2.index = df2.index + 1
        recommendation['restaurants'] = df2.head(10)
    else:
        df2 = pd.DataFrame(suggested_restaurant)
        df2.reset_index(drop=True, inplace=True)
        df2.index = df2.index + 1
        recommendation['restaurants'] = df2.head()

    if len(POI) > 0:
        df3 = pd.DataFrame(POI)
        df3.reset_index(drop=True, inplace=True)
        df3.index = df3.index + 1
        recommendations['POI'] = df3.head(10)
    else:
        if len(suggested_POI) > 0:
            df3 = pd.DataFrame(suggested_POI)
            df3.reset_index(drop=True, inplace=True)
            df3.index = df3.index + 1
            recommendation['suggested_POI'] = df3.head()

    return recommendation



