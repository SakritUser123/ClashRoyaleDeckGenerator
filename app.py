import streamlit as st
from urllib.request import urlopen
from PIL import Image
import time
st.header(" Clash Royale Deck Generator AI")




url = "https://raw.githubusercontent.com/SakritUser123/ClashRoyaleDeckGenerator/refs/heads/main/colored-logo.png"
image = Image.open(urlopen(url))

st.image(image, width=400)
time.sleep(2)  # Show for 2 seconds
st.empty()  # Clear the logo

import streamlit as st

playerID = st.text_input("Enter Player ID: ", key="player_id_key")

st.set_page_config(page_title="Clash Royale App", layout="centered")



if st.button("Predict!"):
   
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")

rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
