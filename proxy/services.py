import requests


class QueryData:
    """
    Получает данные о кандидатах от server.
    Валидирует их и объединяет в общую структуру.
    """

    def __init__(self, url):
        """
        url - роут для получения данных о кандидатах с server
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

    def _get_candidates_skills(self) -> list:
        """
        Итерируется по списку кандидатов, получает подробную инфу по каждому и добавляет в список.
        """
        candidates_skills = []
        candidates_list = self._get_candidates()
        for candidate_name in candidates_list:
            response = requests.get(f"{self.url}/candidates/{candidate_name}")
            if response.status_code == 200:
                candidate_data = response.json()
                candidates_skills.append(candidate_data)
        return candidates_skills

    def get_data(self):
        """
        Валидирует данные полученные с server и в случае ошибки добавляет
        их в error_list
        """
        error_list = []
        result = []
        candidates_skills = self._get_candidates_skills()
        for candidate_data in candidates_skills:
            candidate_data__validated = self._validate_skills(candidate_data)
            if candidate_data__validated:
                result.append(candidate_data)
            else:
                error_list.append(candidate_data)
        error_list_checked = self._check_errors(error_list)
        return result, error_list_checked

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
