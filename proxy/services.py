import requests, json


class QueryData:
    """
    Класс для получения данных от server.
    """

    def __init__(self, url):
        """
        Инициализация класса с конфигами
        """
        self.url = url

    def _get_candidates(self) -> list:
        """
        Получает список кандидатов
        """
        response = requests.get(f"{self.url}/candidates")
        if response.status_code == 200:
            candidates_list = response.json()
            return candidates_list

    def get_candidates_skills(self) -> tuple:
        """
        Итерируется по списку кандидатов, получает подробную инфу по каждому и добавляет в список
        """
        results = []
        error_list = []
        candidates_list = self._get_candidates()
        for candidate_name in candidates_list:
            response = requests.get(f"{self.url}/candidates/{candidate_name}")
            if response.status_code == 200:
                candidate_data = response.json()
                candidate_data__validated = self._validate_skills(candidate_data)
                # Валидируем полученные данные и в случае ошибки добавляем их в error_list
                if candidate_data__validated:
                    results.append(candidate_data)
                else:
                    error_list.append(candidate_data)
        error_list_checked = self._check_errors(error_list)
        return results, error_list_checked

    def _check_errors(self, error_list: list):
        """
        Проверяет список с ошибками, в случае если он пуст - возвращает None
        """
        if len(error_list) == 0:
            return None
        return error_list

    def _validate_skills(self, data: dict) -> bool:
        """
        Валидирует полученные данные
        """
        for name, property in data.items():
            try:
                float(property["skills"])
            except ValueError:
                return False
        return True
