from .services import QueryData
from .config import QueryDataConfig
from flask import Blueprint, jsonify


blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/candidates", methods=["GET"])
def get_candidates():
    """
    Делает запрос на server и возвращает полную информацию о кандидатах
    """
    query = QueryData(QueryDataConfig)
    candidates_data, validation_errors = query.get_data()
    results = jsonify(candidates_data)
    if validation_errors is None:  # вот эту строчку изменять нельзя
        return (results, 200)
    else:
        return (results, 206)
