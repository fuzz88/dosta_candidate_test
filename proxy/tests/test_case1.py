from main import app


client = app.test_client()


def test_get_candidates():
    """
    Тестирует роут get_candidates
    """
    response = client.get("/candidates")
    assert response.status_code == 200


def test_processing_errors(test_error_data):
    """
    Тестирует логику обработки ошибок при валидации данных с server
    """
    assert len(test_error_data) == 3
