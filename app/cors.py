from flask_cors import CORS


def init_cors(app):
    CORS(app, origins=[r".*\.capek.ai"], supports_credentials=True)
