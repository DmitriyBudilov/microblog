import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask

from .models import db, migrate, login

app = Flask(
    import_name=__name__,
    instance_relative_config=False
    )
app.config.from_object("config.DevelopmentConfig")

login.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

if not app.debug:
    # Mail
    # if app.config['MAIL_SERVER']:
    #     auth = None
    #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #         auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    #     secure = ()
    #     if app.config['MAIL_USE_TLS']:
    #         secure = ()
    #     mail_handler = SMTPHandler(
    #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #         fromaddr='no-reply@' + app.config['MAIL_SERVEER'],
    #         toaddrs=app.config['ADMINS'], subject='Microblog Failure',
    #         credentials=auth, secure=secure
    #     )
    #     mail_handler.setLevel(logging.ERROR)
    #     app.logger.addHandler(mail_handler)

    # To File
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


from application import routes, models, errors
