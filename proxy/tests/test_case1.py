from main import app
from services import QueryData
import pytest


client = app.test_client()


def test_get_candidates():
    """
    Тестирует роут get_candidates
    """
    response = client.get("/candidates")
    assert response.status_code == 200


class QueryDataTest(QueryData):
    """
    Класс для тестирования
    """

    @staticmethod
    def test_data():
        """
        Тестовые класс QueryData
        """
        return [
            {"Alice": {"skills": "skills"}},
            {"Dima": {"skills": "skills"}},
            {"Igor": {"skills": 23}},
            {"Viсtor": {"skills": "skills"}},
        ]

    def _get_candidates_skills(self) -> dict:
        """
        Переопределяем метод _get_candidates_skills и передаем в него тестовые данные
        """
        return self.test_data()


def test_errors():
    """
    Тестирует логику обработки ошибок при валидации данных с server
    """
    test_server_client = QueryDataTest("url")
    data, errors = test_server_client.get_data()
    assert len(errors) == 3
