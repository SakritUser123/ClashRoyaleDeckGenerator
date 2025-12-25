import streamlit as st
st.header(" Clash Royale Deck Generator AI")


playerID = st.text_input("Enter Player ID: ", key="player_id_key")


if st.button("Predict!"):
   
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")
st.markdown("""
<style>
/* Target the track of the slider */
div.stSlider > div[data-baseweb="slider"] > div > div {
    background: linear-gradient(to right, #FF0000 0%, #FFA500 25%, #FFFF00 50%, #008000 75%, #0000FF 100%);
}

/* Target the thumb (the movable circle) */
div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
    background-color: #FFFFFF; /* White thumb */
    border: 1px solid #000000;
}
</style>
""", unsafe_allow_html=True)
rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
