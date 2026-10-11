#!/usr/bin/python3
"""Affiche l'id de l'État dont le nom est passé en argument."""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_state import Base, State

if __name__ == "__main__":
    # Arguments : utilisateur, mot de passe, base, nom de l'État cherché
    user, password, database, state_name = sys.argv[1:5]

    # Le moteur sait comment joindre MySQL (localhost, port 3306)
    engine = create_engine(
        "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
            user, password, database),
        pool_pre_ping=True)

    # La session est l'espace de travail pour interroger la base
    Session = sessionmaker(bind=engine)
    session = Session()

    # filter(==) envoie state_name à part : aucune injection SQL possible
    state = session.query(State).filter(State.name == state_name).first()

    # first() renvoie None quand aucune ligne ne correspond
    if state is None:
        print("Not found")
    else:
        print(state.id)

    session.close()     # on libère la connexion
