import streamlit as st

st.set_page_config(page_title="Logiciel de production", page_icon="📦", layout="centered")

st.title("📂 Fichier magasin")

st.write("Renseigne ci-dessous les informations du magasin.")

# On utilise un formulaire pour avoir un vrai bouton "Enregistrer"
with st.form("fiche_magasin"):
    designation_interne = st.text_input("Désignation interne")
    enseigne = st.text_input("Enseigne")
    adresse = st.text_area("Adresse complète")
    raison_sociale = st.text_input("Raison sociale de la société")
    nom_referent = st.text_input("Nom de la personne référente")
    poste_referent = st.text_input("Poste du référent")
    contact_referent = st.text_input("Contact référent (téléphone)")
    mail_facturation = st.text_input("Mail facturation")
    remise_appliquee = st.number_input("Remise appliquée (%)", min_value=0.0, max_value=100.0, step=0.5)

    submit = st.form_submit_button("Enregistrer le magasin")

# Petit stockage en mémoire de session pour voir la liste des magasins saisis
if "magasins" not in st.session_state:
    st.session_state["magasins"] = []

if submit:
    magasin = {
        "Désignation interne": designation_interne,
        "Enseigne": enseigne,
        "Adresse": adresse,
        "Raison sociale": raison_sociale,
        "Nom référent": nom_referent,
        "Poste référent": poste_referent,
        "Contact référent": contact_referent,
        "Mail facturation": mail_facturation,
        "Remise (%)": remise_appliquee,
    }
    st.session_state["magasins"].append(magasin)
    st.success("✅ Magasin enregistré (dans la session).")

# Affichage de la liste des magasins saisis pendant la session
if st.session_state["magasins"]:
    st.subheader("📝 Magasins saisis (session actuelle)")
    st.table(st.session_state["magasins"])
else:
    st.info("Aucun magasin saisi pour le moment.")
