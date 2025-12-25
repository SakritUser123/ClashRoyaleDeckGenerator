import streamlit as st
st.header(" Clash Royale Deck Generator AI")

playerID = st.text_input("Enter Player ID Here: ", "Ex.#ABC123DEF45")

predict_decks = st.button("Predict Deck!", on_click= None)
rating = st.slider("Rate The ouput of the model", min_value=0, max_value=10, value=1, step=1)
st.write(f"Your rating is {rating}")
