#!/usr/bin/python3
"""Lists all State objects from the database using SQLAlchemy."""
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model_state import Base, State

if __name__ == "__main__":
    # Le code ne s'exécute que si on lance le script, pas si on l'importe

    # Connexion à MySQL : dialecte+pilote://user:mot_de_passe@hôte:port/base
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                           .format(sys.argv[1], sys.argv[2], sys.argv[3]),
                           pool_pre_ping=True)

    # sessionmaker crée une "fabrique" de sessions liée à l'engine
    # La session remplace le curseur : c'est elle qui fait les requêtes
    Session = sessionmaker(bind=engine)
    session = Session()

    # query(State) = SELECT * FROM states
    # order_by(State.id) = ORDER BY states.id ASC
    # Chaque élément est un OBJET State, pas un tuple
    for state in session.query(State).order_by(State.id).all():
        print("{}: {}".format(state.id, state.name))

    # Ferme la session pour libérer la connexion
    session.close()
