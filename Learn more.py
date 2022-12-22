import streamlit as st
import pandas as pd

st.title('Some more information on the top 3 highest number of volcano types')

df = pd.read_csv("/Users/nourzein/Desktop/Python/final project/Eruptions.csv")
volcano_counts = df.groupby('Primary Volcano Type').size().reset_index(name='count')
top_types = volcano_counts.nlargest(4, 'count')
st.write(top_types)

import streamlit as st

def display_clickable_image(image_path, link):
    st.markdown(f'<a href="{link}"><img src="{image_path}" alt="link" width="200"></a>', unsafe_allow_html=True)

def strato():
    image_path = ["/Users/nourzein/Desktop/Python/final project/Strato.png",
    "/Users/nourzein/Desktop/Python/final project/stratovolcano.png"]
    st.image(image_path, width=200)
    link = 'https://www.nps.gov/articles/000/composite-volcanoes.htm'
    display_clickable_image(image_path, link)

def shield():
    image_path = ["/Users/nourzein/Desktop/Python/final project/Shieldw.png",
    "/Users/nourzein/Desktop/Python/final project/shield.png"]
    st.image(image_path, width=200)
    link = 'https://www.sciencedirect.com/topics/earth-and-planetary-sciences/shield-volcano'
    display_clickable_image(image_path, link)

def submarine():
    image_path = ["/Users/nourzein/Desktop/Python/final project/Subamirnew.png",
    "/Users/nourzein/Desktop/Python/final project/submarine.png"]
    st.image(image_path, width=200)
    link = "https://earthobservatory.nasa.gov/images/149834/submarine-eruption-of-kavachi-volcano"
    display_clickable_image(image_path, link)

def main():
    strato()
    shield()
    submarine()

main()



