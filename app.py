import streamlit as st
st.header(" Clash Royale Deck Generator AI")



playerID = st.text_input("Enter Player ID: ", key="player_id_key")


if st.button("Predict!"):
   
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")

rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
