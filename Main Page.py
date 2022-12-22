import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
import pydeck as pdk
import plotly.express as px
from PIL import Image


def home(image, df):
    st.title("Volcanic Eruptions Around the World")
    st.write("This site will help you with an array of things to do with volcanoes! It can provide information on volcanic eruptions around the world so you can avoid them when travelling. This site will also help provide information on specific countries and regions that contain volcanoes.")
    st.image(image)
    st.text("The data I will be using is as follows:")
    st.write(df)
    #A stop motion animation
    image1 = Image.open("final project/image1.png")
    image2 = Image.open("final project/image2.png")
    image3 = Image.open("final project/image3.png")
    image4 = Image.open("final project/image4.png")
    img_arrays = [image1, image2, image3, image4]
    loop = True
    placeholder = st.empty()
    while loop:
        for img_array in img_arrays:
            placeholder.image(img_array)
            time.sleep(1)

image = Image.open("final project/volcanoes.png")
df = pd.read_csv("/Users/nourzein/Desktop/Python/final project/Eruptions.csv")


#this bar chart shows how many volcanoes are in each country once you select your region
def region_bar_and_pie_chart():
    region_select_box = st.selectbox("Please select a region", df["Region"].unique())
    region_df = df.loc[df['Region'] == region_select_box, ["Volcano Name", "Country", "Activity Evidence", "Last Known Eruption","Subregion", "Elevation (m)"]]
    country_count = region_df.groupby(['Country'])['Country'].count().to_frame()
    fig, ax = plt.subplots()
    ax.bar(country_count.index, country_count['Country'].values, color = 'red', )
    plt.xticks(rotation=60)
    ax.set_xticklabels(country_count.index, ha="right")
    ax.set_ylabel("Amount of Volcanoes")
    ax.set_title('Number of Volcanos in each Country')
    st.pyplot(fig)
    #thi pie chart then compares the amount of volcanoes in each country in the selected region
    st.title("Compare number of Volcanoes per Country")
    countries_in_region = df.loc[df['Region'] == region_select_box, "Country"].unique()
    country_select_box = st.multiselect("Please select the countries to compare", countries_in_region)
    region_df = df.loc[df['Country'].isin(country_select_box), ["Volcano Name", "Country"]]
    country_counts = region_df.groupby(['Country'])['Country'].count()
    labels = []
    for country, count in country_counts.items():
        label = f"{country}: {count} volcanoes"
        labels.append(label)

    fig = px.pie(country_counts, values='Country', names='Country', title='Number of Volcanoes per Country')
    fig.update_traces(text=country_counts.index)  # Add the labels to the pie chart

    st.plotly_chart(fig)


def elevation_histogram():
    df = pd.read_csv("/Users/nourzein/Desktop/Python/final project/Eruptions.csv")
    elevation_slider = st.slider("select elevation", -6000, 6000, 0)
    elevation_df = df.loc[df["Elevation (m)"] > elevation_slider,:]
    df = df[df["Elevation (m)"] <= elevation_slider]
    #Here, this sorts the table so that it shows the 10 volcanoes with elevations closest to the slider value
    df = df.sort_values(by="Elevation (m)", ascending=True)
    df['diff'] = abs(df['Elevation (m)'] - elevation_slider)
    df = df.sort_values(by='diff')
    st.table(df[["Volcano Name", "Elevation (m)"]].head(10))
    #a histogram here is made based on the slider value as specified above
    fig, ax = plt.subplots()
    bins = 50
    ax.hist(df["Elevation (m)"], bins=bins, color = "red", histtype = "bar", rwidth = 1)
    ax.set_xlabel('Elevation')
    ax.set_ylabel('Amount of Volcanoes')
    ax.set_title('Max Elevation')
    st.pyplot(fig)

def map():
    df = pd.read_csv("/Users/nourzein/Desktop/Python/final project/Eruptions.csv")
    df = df.loc[:, ['Volcano Name', 'Latitude', 'Longitude']]
    df.rename(columns={"Latitude":"lat", "Longitude": "lon"}, inplace= True)
    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Vulcano-fire-icon.svg/640px-Vulcano-fire-icon.svg.png"
    icon_data = {
    "url": ICON_URL,
    "width": 150,
    "height": 150,
    "anchorY": 150
         }
    df["icon_data"]= None
    for i in df.index:
        df["icon_data"][i] = icon_data

    icon_layer = pdk.Layer(type="IconLayer",
                            data = df,
                            get_icon="icon_data",
                            get_position='[lon,lat]',
                            get_size=4,
                            size_scale=10,
                            pickable=True)

    view_state = pdk.ViewState(
             latitude=df["lat"].mean(),
             longitude=df["lon"].mean(),
             zoom=1,
             pitch=0
                 )
    tool_tip = {"html": "Volcano Name:<br/> <b>{Volcano Name}</b>",
                 "style": { "backgroundColor": "red",
                             "color": "white"}
               }
    icon_map = pdk.Deck(
         map_style='mapbox://styles/mapbox/navigation-day-v1',
         layers=[icon_layer],
         initial_view_state= view_state,
         tooltip = tool_tip)

    st.pydeck_chart(icon_map)


def user_input():
    df = pd.read_csv("/Users/nourzein/Desktop/Python/final project/Eruptions.csv")
    df_filter = df.loc[:, ['Volcano Name', 'Activity Evidence','Last Known Eruption']]
    st.title('Want to know more about a specific Volcano?')
    user = st.text_input("type in a volcano you want to know more about")
    df_selected = df_filter[df_filter['Volcano Name'] == user]
    if df_selected.empty:
        st.write('Please type a valid volcano name')
    else:
        st.table(df_selected)


st.sidebar.header("Navigation")
navigation = st.sidebar.selectbox("select from dropdown", ['Home Page','Region Info','Elevation Info','World Map'])
st.sidebar.write(navigation)
if navigation == 'Home Page':
    home(image, df)
elif navigation == 'Region Info':
    st.title('How Many Volcanoes are in each Region?')
    region_bar_and_pie_chart()
elif navigation == 'Elevation Info':
    st.title("Check out the Elevation Levels")
    elevation_histogram()
else:
    st.title("Map of Volcanoes Around the World!")
    map()
    user_input()


