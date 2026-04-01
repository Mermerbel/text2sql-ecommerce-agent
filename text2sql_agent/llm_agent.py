import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# Charge les variables d'environnement (et donc la clé GOOGLE_API_KEY du .env)
load_dotenv()

def get_sql_agent():
    # 1. Connexion à la base de données SQLite avec un chemin absolu (évite les doublons)
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ecommerce.db")
    db_uri = "sqlite:///" + db_path.replace("\\", "/")
    db = SQLDatabase.from_uri(db_uri)
    
    # 2. Initialisation du modèle Google Gemini
    # Utilisation du modèle gemini-2.5-flash qui est disponible pour cette clé
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # 3. Le Toolkit donne à l'agent tous les outils dont il a besoin pour :
    #    - Lister les tables
    #    - Inspecter les schémas des tables pertinentes
    #    - Lancer des requêtes SQL
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    # 4. Création et configuration de l'agent
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="zero-shot-react-description",
        handle_parsing_errors=True
    )
    
    return agent_executor
