import streamlit as st
import time
from urllib.request import urlopen
from PIL import Image

# IMPORTANT: page config must be FIRST
st.set_page_config(page_title="Clash Royale App", layout="centered")

# ---- SPLASH SCREEN ----
splash = st.empty()

with splash.container():
    st.markdown("""
    <style>
    body {
        margin: 0;
        padding: 0;
    }
    
    .splash-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: black;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    
    .splash-image {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        animation: fadeInImage 0.8s ease-in forwards, fadeOutImage 0.8s ease-out forwards 2.5s;
    }
    
    @keyframes fadeInImage {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeOutImage {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }
    </style>
    
    <div class="splash-container">
        <img class="splash-image" src="https://raw.githubusercontent.com/SakritUser123/ClashRoyaleDeckGenerator/main/colored-logo.png">
    </div>
    """, unsafe_allow_html=True)

# Wait for animations to complete
time.sleep(3.5)

# Remove splash
splash.empty()

# ---- MAIN APP ----
st.header("Clash Royale Deck Generator AI")

playerID = st.text_input("Enter Player ID:")

if st.button("Predict!"):
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")

rating = st.slider(
    "Rate the output of the model",
    min_value=0,
    max_value=10,
    value=1,
    step=1
)

st.write(f"Your rating is {rating}")
