import streamlit as st
st.header(" Clash Royale Deck Generator AI")


playerID = st.text_input("Enter Player ID: ", key="player_id_key")

st.markdown("""
  <style>
    body {
        opacity: 0;
        animation: fadeIn 1.2s ease-in forwards;
    }
    @keyframes fadeIn {
        to { opacity: 1; }
    }
  </style>
""", unsafe_allow_html=True)


if st.button("Predict!"):
   
    if playerID:
        st.write(f"You submitted: {playerID}")
    else:
        st.write("Please enter ID before submitting.")

st.header("Rate the output of the model")

rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
