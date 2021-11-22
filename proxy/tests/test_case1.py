from ..main import client

def test_get_candidates():
    """
    Тестирует роут get_candidates
    """
    response = client.get('/candidates')
    assert response.status_code == 200

    

