#!/usr/bin/python3
"""Serveur d'API minimal avec http.server : texte, JSON et erreur 404."""
import http.server
import json

# Port d'écoute demandé par le sujet
PORT = 8000


class SimpleAPIHandler(http.server.BaseHTTPRequestHandler):
    """Choisit la réponse à envoyer selon le chemin demandé."""

    def _reply(self, code, body, content_type):
        """Envoie statut, en-tête, ligne vide et corps au client."""
        self.send_response(code)                        # 1. ligne de statut
        self.send_header("Content-Type", content_type)  # 2. en-tête
        self.end_headers()                              # 3. ligne vide
        self.wfile.write(body.encode("utf-8"))          # 4. corps en octets

    def do_GET(self):
        """Appelée automatiquement à chaque requête GET reçue."""
        # self.path contient le chemin demandé, par exemple "/data"
        if self.path == "/":
            self._reply(200, "Hello, this is a simple API!", "text/plain")
        elif self.path == "/data":
            data = {"name": "John", "age": 30, "city": "New York"}
            # json.dumps transforme le dict Python en texte JSON
            self._reply(200, json.dumps(data), "application/json")
        elif self.path == "/status":
            self._reply(200, "OK", "text/plain")
        elif self.path == "/info":
            info = {"version": "1.0",
                    "description": "A simple API built with http.server"}
            self._reply(200, json.dumps(info), "application/json")
        else:
            # Toute autre route : 404 avec un message explicite
            self._reply(404, "Endpoint not found", "text/plain")


if __name__ == "__main__":
    # "" = écouter sur toutes les adresses de la machine
    server = http.server.HTTPServer(("", PORT), SimpleAPIHandler)
    print("Serving on http://localhost:{}".format(PORT))
    try:
        server.serve_forever()      # attend les requêtes en boucle
    except KeyboardInterrupt:       # Ctrl+C : on arrête proprement
        server.server_close()       # libère le port 8000
