#!/usr/bin/python3
"""API Flask protégée par Basic Auth, par jeton JWT et par rôles."""
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
# Clé secrète qui signe les jetons (au moins 32 caractères)
app.config["JWT_SECRET_KEY"] = "holberton-restful-api-very-strong-secret"

auth = HTTPBasicAuth()      # gestionnaire de l'authentification Basic
jwt = JWTManager(app)       # gestionnaire des jetons JWT

# Utilisateurs en mémoire : on ne stocke que les EMPREINTES des mots de passe
users = {
    "user1": {"username": "user1",
              "password": generate_password_hash("password"),
              "role": "user"},
    "admin1": {"username": "admin1",
               "password": generate_password_hash("password"),
               "role": "admin"},
}


@auth.verify_password
def verify_password(username, password):
    """Renvoie le username si le mot de passe est bon, sinon None."""
    user = users.get(username)
    # check_password_hash compare le mot de passe reçu à l'empreinte
    if user and check_password_hash(user["password"], password):
        return username
    return None             # None = échec : flask_httpauth renvoie 401


@app.route("/basic-protected")
@auth.login_required        # Basic Auth exigée avant d'entrer ici
def basic_protected():
    """Route accessible avec des identifiants Basic valides."""
    return "Basic Auth: Access Granted"


@app.route("/login", methods=["POST"])
def login():
    """Vérifie les identifiants une fois et renvoie un jeton JWT."""
    data = request.get_json(silent=True)        # None si JSON invalide
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid credentials"}), 401
    username = data.get("username")
    password = data.get("password")
    # On réutilise la même vérification que pour Basic Auth
    if not username or not password or not verify_password(username,
                                                           password):
        return jsonify({"error": "Invalid credentials"}), 401
    # L'identité du jeton est une simple chaîne : le username
    token = create_access_token(identity=username)
    return jsonify({"access_token": token})


@app.route("/jwt-protected")
@jwt_required()             # un jeton valide est exigé avant d'entrer ici
def jwt_protected():
    """Route accessible avec un jeton JWT valide."""
    return "JWT Auth: Access Granted"


@app.route("/admin-only")
@jwt_required()
def admin_only():
    """Route réservée aux utilisateurs ayant le rôle admin."""
    username = get_jwt_identity()               # lu dans le jeton
    user = users.get(username)
    # Authentifié mais pas admin : c'est une AUTORISATION refusée -> 403
    if user is None or user["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return "Admin Access: Granted"


# Gestionnaires d'erreurs JWT : toute erreur d'authentification -> 401
@jwt.unauthorized_loader
def handle_unauthorized_error(err):
    """Aucun jeton fourni."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def handle_invalid_token_error(err):
    """Jeton mal formé ou signature fausse."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def handle_expired_token_error(jwt_header, jwt_payload):
    """Jeton expiré (cette fonction reçoit 2 arguments)."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def handle_revoked_token_error(jwt_header, jwt_payload):
    """Jeton révoqué (2 arguments)."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def handle_needs_fresh_token_error(jwt_header, jwt_payload):
    """Jeton frais exigé (2 arguments)."""
    return jsonify({"error": "Fresh token required"}), 401


if __name__ == "__main__":
    app.run()
