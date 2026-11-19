from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["VISITS"] = 0

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/visits")
    def visits():
        app.config["VISITS"] += 1
        return {"visits": app.config["VISITS"]}

    return app