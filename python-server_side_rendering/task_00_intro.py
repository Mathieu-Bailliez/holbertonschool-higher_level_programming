#!/usr/bin/python3
"""Generate personalized invitation files from a template."""


def generate_invitations(template, attendees):
    """Write one invitation file per attendee using the template."""
    # Vérifie que le modèle est une string
    if not isinstance(template, str):
        type_name = type(template).__name__
        print(f"Error: template must be a string, not {type_name}.")
        return

    # Vérifie que attendees est une liste
    if not isinstance(attendees, list):
        type_name = type(attendees).__name__
        print(f"Error: attendees must be a list, not {type_name}.")
        return

    # Vérifie que chaque élément de la liste est un dictionnaire
    for attendee in attendees:
        if not isinstance(attendee, dict):
            type_name = type(attendee).__name__
            print(f"Error: each attendee must be a dict, not {type_name}.")
            return

    # Modèle vide : on arrête sans créer de fichier
    if not template:
        print("Template is empty, no output files generated.")
        return

    # Liste vide : on arrête sans créer de fichier
    if not attendees:
        print("No data provided, no output files generated.")
        return

    # Noms des cases à remplir dans le modèle
    keys = ["name", "event_title", "event_date", "event_location"]

    # Parcourt les participants, avec un numéro qui commence à 1
    for index, attendee in enumerate(attendees, start=1):
        # Repart du modèle intact pour chaque participant
        invitation = template

        # Remplit chaque case du modèle
        for key in keys:
            # Récupère la valeur (None si la clé est absente)
            value = attendee.get(key)
            # Donnée manquante ou None : on met N/A
            if value is None:
                value = "N/A"
            # Remplace la case par la valeur, convertie en string
            invitation = invitation.replace("{" + key + "}", str(value))

        # Construit le nom du fichier de sortie
        filename = f"output_{index}.txt"

        # Écrit l'invitation dans le fichier, en gérant les erreurs
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(invitation)
        except OSError as error:
            print(f"Error: could not write {filename}: {error}")
