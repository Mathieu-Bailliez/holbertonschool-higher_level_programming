#!/usr/bin/python3
"""Renomme en New Mexico l'État dont l'id vaut 2 dans la base."""
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

    # 1. Récupérer l'objet : la session le surveille désormais
    state = session.query(State).filter(State.id == 2).first()

    # On ne modifie que si l'État 2 existe bien
    if state is not None:
        # 2. Modifier l'attribut : la session note l'objet comme modifié
        state.name = "New Mexico"
        # 3. Valider : SQLAlchemy génère et envoie l'UPDATE
        session.commit()

    session.close()     # on libère la connexion
