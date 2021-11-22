import requests, json


class QueryData:
    """
    Класс для получения данных от server.
    """
    def __init__(self, QueryToServerConfig):
        """
        Инициализация класса с конфигами
        """
        configs = QueryToServerConfig()
        self.url = configs.url

    def _get_candidates(self) -> list:
        """
        Получает список кандидатов
        """
        response = requests.get(f"{self.url}/candidates")
        if response.status_code == 200:
            candidates_list = response.json()
            return candidates_list

    def _get_candidates_skills(self) -> tuple:
        """
        Итерируется по списку кандидатов, получает подробную инфу по каждому и добавляет в список
        """
        results = []
        error_count = None
        candidates_list = self._get_candidates()
        for candidate_name in candidates_list:
            response = requests.get(f"{self.url}/candidates/{candidate_name}")
            if response.status_code == 200:
                candidate_data = response.json()
                candidate_data__validated = self._validate_skills(candidate_data)
                # Валидируем полученные данные и в случае ошибки 
                if candidate_data__validated:
                    results.append(candidate_data)
                else:
                    # Возник вопрос: имеет ли смысл error_count делать None, ведь
                    # в случае ошибки валидации нет возможности в самом цикле изменить
                    # тип на список и начать туда добавлять ошибки, так как при 
                    # следующей итерации все перезапишется. Я думаю, будет удобнее
                    # задать error_count = 0, либо пустой список
                    error_count = []
        return results, error_count

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

    def get_data(self) -> tuple:
        """
        Основная функция, которая возвращает подробный список кандидатов и ошибки
        """
        result, errors = self._get_candidates_skills()
        return result, errors
