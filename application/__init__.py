from flask import Flask

from .models import db, migrate

app = Flask(
    import_name=__name__,
    instance_relative_config=False
    )
app.config.from_object("config.DevelopmentConfig")
db.init_app(app)
migrate.init_app(app, db)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from application import routes