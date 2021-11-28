from services import QueryData
import pytest


class QueryDataTest(QueryData):
    """
    Класс для тестирования
    """

    @staticmethod
    def test_data():
        """
        Тестовый класс QueryData
        """
        return [
            {"Alice": {"skills": "skills", "tools": ["python"]}},
            {"Dima": {"skills": "skills", "tools": ["python"]}},
            {"Igor": {"skills": 23, "tools": []}},
            {"Anton": {"skills": 3.2, "tools": ["python"]}},
            {"Viсtor": {"skills": "skills", "tools": ["python"]}},
        ]

    def _get_candidates_skills(self) -> dict:
        """
        Переопределяем метод _get_candidates_skills и передаем в него тестовые данные
        """
        return self.test_data()


@pytest.fixture()
def test_error_data():
    """
    Фикстура для создания экземпляра тестового класса
    """
    test_server_client = QueryDataTest("url")
    data, errors = test_server_client.get_data()
    return errors
