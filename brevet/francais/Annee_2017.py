import streamlit as st

def main():
    st.title("Français 2017")
    #Button for back to main page
    if st.button("Retour", key="retour"):
        st.session_state.current_page = ''
        st.rerun()