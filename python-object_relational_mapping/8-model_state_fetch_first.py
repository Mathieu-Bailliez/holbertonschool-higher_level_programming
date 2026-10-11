#!/usr/bin/python3
"""Prints the first State object from the database using SQLAlchemy."""
import sys
from model_state import Base, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    # Le code ne s'exécute que si on lance le script, pas si on l'importe

    # Connexion à MySQL : dialecte+pilote://user:mot_de_passe@hôte:port/base
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                           .format(sys.argv[1], sys.argv[2], sys.argv[3]),
                           pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # order_by(State.id) garantit l'ordre, sinon "le premier" n'a pas de sens
    # first() = LIMIT 1 : MySQL ne renvoie qu'UNE ligne (pas tout le tableau)
    # Renvoie un objet State, ou None si la table est vide
    state = session.query(State).order_by(State.id).first()

    # Toujours tester None avant d'utiliser l'objet, sinon crash
    if state is None:
        print("Nothing")
    else:
        print("{}: {}".format(state.id, state.name))

    session.close()
