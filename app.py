import streamlit as st
from urllib.request import urlopen
from PIL import Image
st.header(" Clash Royale Deck Generator AI")


playerID = st.text_input("Enter Player ID: ", key="player_id_key")

st.set_page_config(page_title="Clash Royale App", layout="centered")


url = "https://raw.githubusercontent.com/SakritUser123/ClashRoyaleDeckGenerator/refs/heads/main/colored-logo.png"
image = Image.open(urlopen(url))


import streamlit as st

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
}

#splash img {
    width: 400px;
    z-index: 10000; /* make sure image is above everything */
}

/* Fade out animation */
.fade-out {
    animation: fadeout 2s forwards;
}

@keyframes fadeout {
    from {opacity: 1;}
    to {opacity: 0; visibility: hidden;}
}
</style>

<div id="splash">
    <img src=image>
</div>

<script>
    // Wait 2 seconds, then fade out
    setTimeout(function(){
        document.getElementById('splash').classList.add('fade-out');
    }, 2000);
    // Remove splash from DOM after fade
    setTimeout(function(){
        var splash = document.getElementById('splash');
        if (splash) splash.remove();
    }, 4000);
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
