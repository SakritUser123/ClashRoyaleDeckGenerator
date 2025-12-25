import streamlit as st
st.header(" Clash Royale Deck Generator AI")


playerID = st.text_input("Enter Player ID: ", key="player_id_key")

st.set_page_config(page_title="Clash Royale App", layout="centered")


from urllib.request import urlopen
from PIL import Image

url = "https://raw.githubusercontent.com/username/repo/branch/colored-logo.png"
image = Image.open(urlopen(url))

st.image(image, width=400)

