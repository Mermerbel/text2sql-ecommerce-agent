import os
from datetime import datetime, timedelta
import random
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# --- Modèles de base de données ---
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    city = Column(String)
    country = Column(String)
    signup_date = Column(DateTime)
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime)
    total_amount = Column(Float)
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


def init_db(db_name="ecommerce.db"):
    # Chemin absolu du dossier actuel pour forcer la création au bon endroit
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
    
    # Supprime physiquement l'ancien fichier s'il existe (remplacement total)
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("Ancienne base de données supprimée.")
        except OSError:
            pass

    # SQLAlchemy requiert des slashs (/) plutôt que des anti-slashs (\) sous Windows
    db_uri = "sqlite:///" + db_path.replace("\\", "/")
    
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    return engine

def seed_db(engine, num_users=500, num_products=50, num_orders=1500):
    Session = sessionmaker(bind=engine)
    session = Session()
    fake = Faker('fr_FR')

    print("Création des utilisateurs...")
    users = []
    for _ in range(num_users):
        u = User(
            name=fake.name(),
            email=fake.email(),
            city=fake.city(),
            country='France',
            signup_date=fake.date_time_between(start_date='-2y', end_date='now')
        )
        users.append(u)
    session.add_all(users)
    session.commit()

    print("Création des produits...")
    catalog = {
        'Électronique': ['Smartphone', 'Laptop', 'Casque Audio', 'Montre', 'Tablette', 'Enceinte'],
        'Vêtements': ['T-shirt', 'Jeans', 'Veste', 'Robe', 'Pull', 'Baskets', 'Manteau'],
        'Maison': ['Canapé', 'Lampe', 'Tapis', 'Cafetière', 'Aspirateur', 'Table', 'Chaise'],
        'Loisirs': ['Vélo', 'Tente', 'Raquette', 'Guitare', 'Jeu de Société', 'Livre'],
        'Beauté': ['Crème Visage', 'Parfum', 'Mascara', 'Sérum', 'Shampoing', 'Savon']
    }
    categories = list(catalog.keys())
    products = []
    
    for _ in range(num_products):
        cat = random.choice(categories)
        base_name = random.choice(catalog[cat])
        adj = random.choice(['Pro', 'Max', 'Premium', 'Eco', 'Ultra', 'Plus', 'Classic', ''])
        name = f"{base_name} {adj}".strip()
        
        p = Product(
            name=name,
            category=cat,
            price=round(random.uniform(15.0, 500.0), 2)
        )
        products.append(p)
    session.add_all(products)
    session.commit()

    print("Création des commandes et articles...")
    orders = []
    order_items = []
    for _ in range(num_orders):
        user = random.choice(users)
        order_date = fake.date_time_between(start_date=user.signup_date, end_date='now')
        
        o = Order(user_id=user.id, order_date=order_date, total_amount=0)
        orders.append(o)
        session.flush() # pour obtenir l'ID de la commande
        
        num_items = random.randint(1, 5)
        order_total = 0
        for _ in range(num_items):
            product = random.choice(products)
            qty = random.randint(1, 3)
            price = product.price
            order_total += price * qty
            
            oi = OrderItem(order_id=o.id, product_id=product.id, quantity=qty, unit_price=price)
            order_items.append(oi)
            
        o.total_amount = round(order_total, 2)

    session.add_all(orders)
    session.add_all(order_items)
    session.commit()
    print("Base de données générée avec succès !")

if __name__ == "__main__":
    print("Initialisation du squelette de la base de données...")
    db_engine = init_db("ecommerce.db")
    seed_db(db_engine)
