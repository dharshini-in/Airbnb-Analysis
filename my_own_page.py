#importing libraries
import pandas as pd
import pymongo
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image

#setting up page configuration
st.set_page_config(page_title = "Airbnb Data Visualization",
                   layout = "wide",
                   initial_sidebar_state = "expanded",
                   menu_items={'About': """# The dashboard app is created !"""}
)

#setting up title
st.title("Airbnb Analysis", anchor=None)
st.divider()

#Creating option menu in side bar
with st.sidebar:
    selected = option_menu("Menu", ["HOME","STATISTICS","ANALYSIS"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#517fc9"},
                                   "nav-link-selected": {"background-color": "#517fc9"}}
                          )
    

# Reading the cleaned dataframe
df = pd.read_csv(r'D:\Desktop\airbnb\airbnb_data.csv')

# Home page
if selected == "HOME":
    
    st.image(Image.open(r"D:\download.jpg"), use_column_width=True)

    st.markdown("##### :blue[INTRODUCTION]")
    st.write("Airbnb is an online marketplace that connects people who want to rent out their property with people who are looking for accommodations,typically for short stays.Airbnb offers hosts a relatively easy way toearn some income from their property.Guests often find that Airbnb rentals are cheaper and homier than hotels.")
    
    st.markdown("##### :blue[PROBLEM STATEMENT]")
    st.write("This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends")
    
    st.markdown("##### :blue[OBJECTIVE]")
    st.write('''The project involves cleaning and preparing the Airbnb dataset, developing a Streamlit web app for interactive exploration of listings, conducting price and availability analysis using dynamic visualizations, investigating location-based insights''')

# STATISTICS PAGE
if selected == "STATISTICS":
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a country', sorted(df.country.unique()), sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select property_type', sorted(df.property_type.unique()), sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select room_type', sorted(df.room_type.unique()), sorted(df.room_type.unique()))
    price = st.slider('Select price', df.price.min(), df.price.max(), (df.price.min(), df.price.max()))

    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

    # TOP 10 PROPERTY TYPES BAR CHART
    df1 = df.query(query).groupby(["property_type"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
    fig = px.bar(df1,
                 title='Top 10 Property Types',
                 x='Listings',
                 y='property_type',
                 orientation='h',
                 color='property_type',
                 color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig, use_container_width=True)

    # TOP 10 HOSTS BAR CHART
    df2 = df.query(query).groupby(["host_name"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
    fig = px.bar(df2,
                 title='Top 10 Hosts with Highest number of Listings',
                 x='Listings',
                 y='host_name',
                 orientation='h',
                 color='host_name',
                 color_continuous_scale=px.colors.sequential.Agsunset)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
    df1 = df.query(query).groupby(["room_type"]).size().reset_index(name="counts")
    fig = px.pie(df1,
                 title='Total Listings in each room_types',
                 names='room_type',
                 values='counts',
                 color_discrete_sequence=px.colors.sequential.Rainbow
                 )
    fig.update_traces(textposition='outside', textinfo='value+label')
    st.plotly_chart(fig, use_container_width=True)

    # TOTAL LISTINGS BY country CHOROPLETH MAP
    country_df = df.query(query).groupby(['country'], as_index=False)['name'].count().rename(columns={'name': 'Total_Listings'})
    fig = px.choropleth(country_df,
                        title='Total Listings in each country',
                        locations='country',
                        locationmode='country names',
                        color='Total_Listings',
                        color_continuous_scale=px.colors.sequential.Plasma
                        )
    st.plotly_chart(fig, use_container_width=True)

    #REVIEW SCORE IN ROOM TYPE:
    import plotly.express as px

    # Grouping by room_type and calculating mean review_scores
    rev_df = df.groupby('room_type', as_index=False)['review_scores'].mean().sort_values(by='review_scores')

    # Create the choropleth map
    fig = px.bar(rev_df, x='room_type', y='review_scores', 
                title='Average Review Scores by Room Type', 
                labels={'room_type': 'Room Type', 'review_scores': 'Average Review Scores'}, 
                color='review_scores',
                color_continuous_scale='Viridis')

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)

    #PRICE IN ROOM TYPE:
    # Importing Plotly Express
    import plotly.express as px

    # Calculate the average price by room type
    pr_df = df.groupby('room_type', as_index=False)['price'].mean().sort_values(by='price')

    # Create the bar chart using Plotly Express
    fig = px.bar(pr_df, x='room_type', y='price', title='Average Price by Room Type', labels={'room_type': 'Room Type', 'price': 'Average Price'})
    fig.update_layout(xaxis_title='Room Type', yaxis_title='Average Price')

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

# ANALYSIS PAGE
if selected == "ANALYSIS":
    st.markdown("## ANALYSIS more about the Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a country',sorted(df.country.unique()),sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select property_type',sorted(df.property_type.unique()),sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
    price = st.slider('Select price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
    
    
    # AVG price BY ROOM TYPE BARCHART
    pr_df = df.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
    fig = px.bar(data_frame=pr_df,
                 x='room_type',
                 y='price',
                 color='price',
                 title='Avg price in each Room type'
                )
    st.plotly_chart(fig,use_container_width=True)
   
    
    # AVG price IN COUNTRIES SCATTERGEO
    country_df = df.query(query).groupby('country',as_index=False)['price'].mean()
    fig = px.scatter_geo(data_frame=country_df,
                                   locations='country',
                                   color= 'price', 
                                   hover_data=['price'],
                                   locationmode='country names',
                                   size='price',
                                   title= 'Avg price in each country',
                                   color_continuous_scale='agsunset'
                        )
    st.plotly_chart(fig,use_container_width=True)
    
    # BLANK SPACE
    st.markdown("#   ")
    st.markdown("#   ")
    
    # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
    country_df = df.query(query).groupby('country',as_index=False)['availability_365'].mean()
    country_df.availability_365 = country_df.availability_365.astype(int)
    fig = px.scatter_geo(data_frame=country_df,
                                   locations='country',
                                   color= 'availability_365', 
                                   hover_data=['availability_365'],
                                   locationmode='country names',
                                   size='availability_365',
                                   title= 'Avg Availability in each country',
                                   color_continuous_scale='agsunset'
                        )
    st.plotly_chart(fig,use_container_width=True)

    
    # Availability by Room Type Pie Chart
    availability_by_room_type = df.query(query).groupby('room_type')['availability_365'].mean().reset_index()
    fig = px.pie(availability_by_room_type,
                names='room_type',
                values='availability_365',
                title='Average Availability by Room Type',
                labels={'availability_365': 'Average Availability (in days)', 'room_type': 'Room Type'},
                color='room_type',
                color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig, use_container_width=True)
