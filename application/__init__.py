from flask import Flask
from flask_login import LoginManager

from .models import db, migrate, login

app = Flask(
    import_name=__name__,
    # instance_relative_config=False
    )
app.config.from_object("config.DevelopmentConfig")

login.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

from application import routes
