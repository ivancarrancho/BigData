from config import SECRET_KEY
from cors import init_cors
# from .errors import register_errors
# from ..api.api_v1.api import register_blueprints
# from ..api.api_v1.docs import register_doc
# from .jwt import init_jwt


def init_app(app):
    init_cors(app)
    # register_errors(app)
    # init_jwt(app)
    # register_blueprints(app)
    # register_docs(docs)
    app.config['SECRET_KEY'] = SECRET_KEY
