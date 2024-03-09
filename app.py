import streamlit as st
import importlib
import json

# Load subjects from matieres.json
def load_matieres():
    with open('matieres.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def import_annee(matiere_path, annee):
    module_path = f"{matiere_path}.Annee_{annee}"
    module = importlib.import_module(module_path)
    return module

def main():
    st.set_page_config(page_title="Préparation au Brevet et Bac", initial_sidebar_state="collapsed", layout="centered")
    matieres = load_matieres()

    if 'current_page' not in st.session_state:
        st.session_state.current_page = ''

    if st.session_state.current_page == '':
        st.title("Préparation au Brevet et Bac")
        exam_type = st.radio("Choisir le type d'examen", list(matieres.keys()))
        display_tabs(exam_type, matieres)
    else:
        display_content()

def display_tabs(exam_type, matieres):
    selected_exam = matieres[exam_type]
    # If maintenance is active change emoji to a warning sign
    for matiere, info in selected_exam.items():
        if info.get("Maintenance", False):
            info["emoji"] = "⚠️"

    tab_labels = [f"{info['emoji']} {matiere}" for matiere, info in selected_exam.items() if info['active']]
    
    # Show a warning if there are no active subjects
    if not tab_labels:
        st.warning("⚠️ Aucune matière actuellement disponible. Merci de revenir plus tard.")
        return

    # Create tabs for each active subject
    tabs = st.tabs(tab_labels)

    for tab, (matiere, info) in zip(tabs, selected_exam.items()):
        if not info['active']:  # Skip inactive subjects
            continue
        with tab:
            st.header(matiere)
            if info.get("Maintenance", False):
                # Display maintenance message
                st.warning(info.get("message_content", "⚠️ Cette matière est actuellement en maintenance. Veuillez revenir plus tard."))
                continue  # Skip displaying years if in maintenance mode
            # Display years and content normally for active subjects not in maintenance
            # If Message is True, display the message content
            if info.get("Message", False):
                st.warning(info.get("message_content", "⚠️"))
            for annee in range(2023, info["start_year"] - 1, -1):
                if annee in info["bypass_years"]:
                    continue
                button_label = f"Commencer l'entraînement pour l'année **{annee}**"
                unique_key = f"{info['path']}_{annee}_button"
                if st.button(button_label, key=unique_key):
                    st.session_state.current_page = f"{info['path']}_{annee}"
                    st.experimental_rerun()

def display_content():
    path, annee = st.session_state.current_page.rsplit("_", 1)
    page_module = import_annee(path, annee)
    page_module.main()

if __name__ == "__main__":
    main()

