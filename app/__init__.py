import os
from flask import Flask
from flask_marshmallow import Marshmallow
from constants import AppSettings
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from app.celery_utils import make_celery


app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', AppSettings.TESTING))

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN', ''),
    integrations=[FlaskIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=.75,
    environment=app.config.get('ENV')
)

print(app.config)
ma = Marshmallow(app)
celery = make_celery(app)
app.celery = celery

# import logging
# logging.basicConfig(filename='logs.txt',
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)

from app.v1.blueprint import v1_api  # import must come later to avoid circular dependency
app.register_blueprint(v1_api, url_prefix='/v1/')
print(app.url_map)
