from flask_cors import CORS


def init_cors(app):
    CORS(app, origins=['*'], supports_credentials=True)
