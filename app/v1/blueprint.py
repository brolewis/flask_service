from flask import Blueprint
from app.v1.healthcheck import healthcheck
from app.v1.quotes import get_quote


v1_api = Blueprint('v1_api', __name__)

v1_api.add_url_rule(
        "/healthcheck/",
        view_func=healthcheck,
        methods=['GET'])

v1_api.add_url_rule("/quote", view_func=get_quote, methods=["GET"])
