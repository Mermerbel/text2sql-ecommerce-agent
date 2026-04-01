import streamlit as st
from llm_agent import get_sql_agent

# -- Header et Configuration de page --
st.set_page_config(
    page_title="Assistant Data E-Commerce", 
    page_icon="https://cdn-icons-png.flaticon.com/512/8539/8539259.png", 
    layout="centered"
)

st.title("Assistant Data E-Commerce")
st.markdown("""
Bienvenue sur l'agent **Text-to-SQL**. Cet outil utilise l'intelligence artificielle (Google Gemini) pour traduire 
vos questions naturelles en requêtes SQL, interroger la base de données e-commerce, et formuler une réponse.
""")

# -- Initialisation de l'Agent --
if "agent" not in st.session_state:
    with st.spinner("Création de la connexion AI-Database..."):
        try:
            st.session_state.agent = get_sql_agent()
        except Exception as e:
            st.error(f"Erreur d'initialisation : {e}")
            st.stop()

# -- Historique du chat --
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Bonjour ! Je suis connecté à la base de données (Utilisateurs, Produits, Commandes). Que souhaitez-vous analyser aujourd'hui ? (Ex: Quel est notre produit le plus cher ?)"}
    ]

# Restituer les anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -- Input Utilisateur --
if prompt := st.chat_input("Votre question..."):
    # Affichage de la question
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exécution de la requête via l'agent
    with st.chat_message("assistant"):
        with st.spinner("Consultation de la base de données via SQL..."):
            try:
                # L'agent fait tout le travail : compréhension, génération de sql, exécution, formulation de la réponse
                response = st.session_state.agent.invoke({"input": prompt})
                output_text = response["output"]
                
                # Afficher le résultat final
                st.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
            except Exception as e:
                error_msg = f"❌ Une erreur interne est survenue : `{str(e)}`"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
