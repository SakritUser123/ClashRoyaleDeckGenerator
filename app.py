import streamlit as st
st.header(" Clash Royale Deck Generator AI")


playerID = st.text_input("Enter Player ID: ", key="player_id_key")

import time

# Hide Streamlit default menu and footer
st.set_page_config(page_title="Clash Royale App", page_icon=":crossed_swords:", layout="centered")

# CSS for full screen black background
st.markdown("""
    <style>
    .splash {
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
        transition: opacity 2s;
    }
    </style>
""", unsafe_allow_html=True)

# Add the splash screen with the logo
st.markdown("""
    <div class="splash" id="splash">
        <img src="https://upload.wikimedia.org/wikipedia/en/6/6b/Clash_Royale_logo.png" width="400">
    </div>
""", unsafe_allow_html=True)

# Wait a few seconds then fade out
time.sleep(2)

# Use JavaScript to fade out the logo
st.markdown("""
<script>
document.getElementById('splash').style.opacity = '0';
setTimeout(function(){document.getElementById('splash').style.display='none';}, 2000);
</script>
""", unsafe_allow_html=True)



if st.button("Predict!"):
   
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")

rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
