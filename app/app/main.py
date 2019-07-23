from flask import Flask
from app_setup import init_app
from db import database

app = Flask(__name__)
init_app(app)

bucket = database.get_default_bucket()
# bucket.n1ql_query("CREATE PRIMARY INDEX ON `app`").execute()
# bucket.n1ql_query("CREATE INDEX `Mes` ON `app`(`Mes`)").execute()
# bucket.n1ql_query("CREATE INDEX `type` ON `app`(`type`)").execute()
# bucket.n1ql_query("CREATE INDEX `Segmento` ON `app`(`Segmento`)").execute()
# bucket.n1ql_query("CREATE INDEX `Zona` ON `app`(`Zona`)").execute()
# bucket.n1ql_query("CREATE INDEX `Ano` ON `app`(`Ano`)").execute()
