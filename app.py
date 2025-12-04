import streamlit as st
from fpdf import FPDF
import pandas as pd

# ------------------------ CONFIG ------------------------
st.set_page_config(
    page_title="Logiciel de production Shoyo",
    page_icon="📦",
    layout="centered"
)

# ------------------------ SESSION STATE ------------------------
if "clients" not in st.session_state:
    st.session_state["clients"] = []  # Liste contenant les fiches clients


# ------------------------ FONCTION : CREATION PDF ------------------------
def create_client_pdf(client: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Fiche client", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "", 12)

    for key, value in client.items():
        texte = f"{key} : {value}"
        pdf.multi_cell(0, 8, texte)
        pdf.ln(1)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return pdf_bytes


# ------------------------ NAVIGATION ------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Création fichier client", "Fichier client"]
)


# ------------------------ PAGE 1 : CRÉATION CLIENT ------------------------
if page == "Création fichier client":

    st.title("🧾 Création fichier client")
    st.write("Renseigne ci-dessous les informations du client / magasin.")

    with st.form("fiche_client"):
        designation_interne = st.text_input("Désignation interne")
        enseigne = st.text_input("Enseigne")
        adresse = st.text_area("Adresse complète")
        raison_sociale = st.text_input("Raison sociale de la société")
        nom_referent = st.text_input("Nom de la personne référente")
        poste_referent = st.text_input("Poste du référent")
        contact_referent = st.text_input("Contact référent (téléphone)")
        mail_facturation = st.text_input("Mail facturation")
        remise_appliquee = st.number_input(
            "Remise appliquée (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.5
        )

        submit = st.form_submit_button("Enregistrer le fichier client")

    if submit:
        client = {
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
        st.session_state["clients"].append(client)
        st.success("✅ Fiche client enregistrée !")


# ------------------------ PAGE 2 : FICHIER CLIENT ------------------------
elif page == "Fichier client":

    st.title("📂 Fichier client")

    if not st.session_state["clients"]:
        st.info("Aucune fiche client enregistrée pour le moment.")
    else:
        df = pd.DataFrame(st.session_state["clients"])

        st.subheader("Récapitulatif des fichiers clients")
        st.dataframe(df, use_container_width=True)

        st.subheader("Téléchargement PDF")
        for idx, client in enumerate(st.session_state["clients"]):
            with st.expander(f"Fiche client #{idx + 1} - {client.get('Désignation interne', '')}"):

                st.write(client)

                pdf_bytes = create_client_pdf(client)

                st.download_button(
                    label="📄 Télécharger cette fiche en PDF",
                    data=pdf_bytes,
                    file_name=f"fiche_client_{idx + 1}.pdf",
                    mime="application/pdf",
                    key=f"pdf_{idx}"
                )
