#!/usr/bin/python3
"""Affiche toutes les villes avec le nom de leur État, triées par id."""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_state import Base, State
from model_city import City

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

    # On demande des paires (State, City), on ne garde que celles
    # où l'id de l'État correspond au state_id de la ville (jointure),
    # puis on trie par id de ville
    rows = (session.query(State, City)
            .filter(State.id == City.state_id)
            .order_by(City.id)
            .all())

    # Chaque résultat est un tuple : on le "déballe" en deux variables
    for state, city in rows:
        print("{}: ({}) {}".format(state.name, city.id, city.name))

    session.close()     # on libère la connexion
