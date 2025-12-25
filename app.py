import streamlit as st
st.header(" Clash Royale Deck Generator AI")


playerID = st.text_input("Enter Player ID: ", key="player_id_key")

import time

st.set_page_config(page_title="Clash Royale App", layout="centered")

# Create a container for the splash screen
splash = st.empty()

# URL of Clash Royale logo
logo_url = "https://upload.wikimedia.org/wikipedia/en/6/6b/Clash_Royale_logo.png"

# Fade-out effect: gradually reduce opacity
for opacity in range(100, -1, -5):
    splash.markdown(
        f"""
        <div style="
            background-color:black;
            width:100vw;
            height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
        ">
            <img src="{logo_url}" style="width:400px; opacity:{opacity/100}; transition: opacity 0.2s;">
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.05)

# Remove splash
splash.empty()



if st.button("Predict!"):
   
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")

rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
