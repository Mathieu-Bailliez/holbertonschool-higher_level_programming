#!/usr/bin/python3
"""Ajoute l'État Louisiana à la base puis affiche son nouvel id."""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_state import Base, State

if __name__ == "__main__":
    # Arguments : utilisateur, mot de passe, nom de la base
    user, password, database = sys.argv[1:4]

    # Le moteur sait comment joindre MySQL (localhost, port 3306)
    engine = create_engine(
        "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
            user, password, database),
        pool_pre_ping=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Créer l'objet : il n'existe encore qu'en mémoire, son id vaut None
    new_state = State(name="Louisiana")
    # 2. Le confier à la session (le "panier")
    session.add(new_state)
    # 3. Valider : SQLAlchemy envoie l'INSERT, MySQL attribue l'id
    session.commit()

    # Après le commit, l'id choisi par MySQL est rangé dans l'objet
    print(new_state.id)

    session.close()     # on libère la connexion
