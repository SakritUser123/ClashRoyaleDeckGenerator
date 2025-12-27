import streamlit as st
import time
from urllib.request import urlopen
from PIL import Image

# IMPORTANT: page config must be FIRST
st.set_page_config(page_title="Clash Royale App", layout="centered")

# ---- SPLASH SCREEN ----
splash = st.empty()

splash.markdown("""
<style>
#splash {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: black;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    animation: fadeout 3s ease-in forwards;
    animation-delay: 2s;
}

#splash img {
    width: 400px;
    animation: fadein 0.5s ease-in forwards;
}

@keyframes fadein {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeout {
    from { opacity: 1; }
    to { opacity: 0; visibility: hidden; }
}
</style>

<div id="splash">
    <img src="https://raw.githubusercontent.com/SakritUser123/ClashRoyaleDeckGenerator/main/colored-logo.png">
</div>
""", unsafe_allow_html=True)

# Keep splash visible during animation
time.sleep(5)

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
