import streamlit as st
st.header(" Clash Royale Deck Generator AI")


playerID = st.text_input("Enter Player ID: ", key="player_id_key")

st.set_page_config(page_title="Clash Royale App", layout="centered")

# Splash screen HTML + CSS
st.markdown("""
    <style>
        /* Fullscreen overlay */
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
            animation: fadeout 3s forwards;
            animation-delay: 2s; /* Show logo for 2 seconds before fading */
        }

        #splash img {
            width: 400px;
        }

        @keyframes fadeout {
            from {opacity: 1;}
            to {opacity: 0; visibility: hidden;}
        }
    </style>

    <div id="splash">
        <img src="colored-logo.png">
    </div>
""", unsafe_allow_html=True)




if st.button("Predict!"):
   
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")

rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
