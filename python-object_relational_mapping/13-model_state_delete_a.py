#!/usr/bin/python3
"""Supprime de la base tous les États dont le nom contient la lettre a."""
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

    # 1. Récupérer tous les États dont le nom contient un "a"
    #    (% = n'importe quelle suite de caractères, même vide)
    states = session.query(State).filter(State.name.like("%a%")).all()

    # 2. Marquer chacun "à supprimer" dans la session
    for state in states:
        session.delete(state)

    # 3. Valider : SQLAlchemy envoie les DELETE à MySQL
    session.commit()

    session.close()     # on libère la connexion
