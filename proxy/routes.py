from services import QueryData
from config import QueryDataConfig
from flask import Blueprint, jsonify


blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/candidates", methods=["GET"])
def get_candidates():
    """
    Делает запрос на server и возвращает полную информацию о кандидатах
    """
    configs = QueryDataConfig()
    server_client = QueryData(configs.url)
    candidates_data, validation_errors = server_client.get_data()
    result = jsonify(candidates_data)
    if validation_errors is None:  # вот эту строчку изменять нельзя
        return (result, 200)
    else:
        return (result, 206)
