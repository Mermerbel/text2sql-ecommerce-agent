# Assistant Data E-Commerce (Agent Text-to-SQL)

> **Projet Personnel - Master 2 Spécialité Bases de Données & IA**
> *Ce projet a été réalisé dans un but de formation et de démonstration technique pour mon portfolio. Il illustre la double compétence nécessaire aujourd'hui : la modélisation classique de bases de données relationnelles combinée au déploiement des modèles d'Intelligence Artificielle Générative (LLM).*

## Présentation du Projet

Cet outil est un assistant conversationnel (chatbot) permettant d'interroger une base de données e-commerce complexe à l'aide de questions en **langage courant** (ex: *"Combien a-t-on vendu d'articles au total pour la catégorie Électronique ?"*).

Au lieu de faire appel à un Data Analyst, l'utilisateur pose sa question et l'agent intelligent se charge de :
1. Comprendre l'intention en lisant le nom des tables.
2. Écrire la requête `SQL` correspondante (impliquant souvent des requêtes de groupes ou jointures - `JOIN`, `GROUP BY`).
3. Tester la requête sur la base localement et se corriger si le moteur SQL lève une exception.
4. Synthétiser la réponse en français.

## Stack Technique

*   **Gestion de la Donnée** : `SQLite` + `SQLAlchemy` avec de fausses données riches générées via `Faker`.
*   **Intelligence Artificielle** : API de **Google Gemini** (modèle `gemini-2.5-flash`).
*   **Middleware IA** : Framework **LangChain** et son SQL Agent Toolkit.
*   **Interface Web** : **Streamlit** (Frontend interactif rapide en Python).

---

## Installation & Démarrage (Windows)

### 1. Cloner et préparer l'environnement
Ouvrez votre terminal (Prompt ou PowerShell) et assurez-vous de **vous placer dans le dossier du projet** avant de taper la moindre commande :
```bash
cd c:\Users\belas\Documents\Fac\Master\M2\Projet_Perso\text2sql_agent
```

Installez ensuite les dépendances listées dans le projet (avec la commande Windows `py`) :
```bash
py -m pip install -r requirements.txt
```

### 2. Configurer la Clé API
Assurez-vous qu'un fichier `.env` est présent à la racine de votre dossier projet, contenant votre clé d'API personnelle (sans guillemets) :
```env
GOOGLE_API_KEY=votre_clef_ici
```

### 3. Générer la Base de Données Fake Data
Le schéma contient 4 tables (`users`, `orders`, `products`, `order_items`). Pour les injecter :
```bash
py setup_db.py
```
*Cela créera un fichier `ecommerce.db` à la racine.*

### 4. Démarrer l'interface 
**Attention :** Un projet Streamlit ne se lance jamais avec une simple commande de type `python app.py`. Il faut absolument passer par le moteur Streamlit :

```bash
py -m streamlit run app.py
```
> L'application s'ouvrira immédiatement dans votre navigateur par défaut à l'adresse locale http://localhost:8501.

---

## Idées de "Stress Tests"
Testez l'agent avec des questions "pièges" pour vérifier la qualité des agents LangChain :
- *"Donne-moi le top 3 des produits les plus chers en ordre décroissant."*
- *"Quelle est l'adresse mail du client qui a fait la commande la plus onéreuse ?"*
