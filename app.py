import streamlit as st
#st.header(" Clash Royale Deck Generator AI")


import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Clash Royale AI Agent",
    page_icon="🃏",
    layout="centered"
)

# --- SPLASH SCREEN ---
splash = st.empty()  # placeholder for splash

logo_text = "🃏 Clash Royale AI Agent"

# Display splash screen with black background
for opacity in [1, 0.8, 0.6, 0.4, 0.2, 0]:
    splash.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: black;
            flex-direction: column;
        ">
            <h1 style="color:white; font-size:60px; opacity:{opacity}; transition: opacity 0.3s;">{logo_text}</h1>
            <progress value="{1-opacity}" max="1" style="width:300px; height:20px;"></progress>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.3)

# Clear splash
splash.empty()

# --- MAIN APP ---
st.title("Welcome to Clash Royale AI Agent!")
st.write(
    "Generate balanced decks, check player stats, and interact with the Clash Royale API using AI."
)

# Example input for player stats
player_tag = st.text_input("Enter player tag (e.g., #ABC123):")
if player_tag:
    st.wr



playerID = st.text_input("Enter Player ID: ", key="player_id_key")


if st.button("Predict!"):
   
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")

rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
