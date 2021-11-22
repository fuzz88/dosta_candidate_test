import requests, json


# нейминг объектов самое интересное в программировании)
# названия должны кратчайшим способом описывать финальное предназначение объекта.
# это важно для читаемости. твой вариант не плох, но
# смотри какие ещё есть: ServerData, ExternalAPI, QueryData ...
class QueriesToServer:
    """
    Здесь всегда должен располагаться doc-string, который описывает назначение класса.

    Например:
    класс для получения данных от server.

    также производит валидацию данных. при ошибке валидации выкидывает CustomValidationError.
    """

    def __init__(self, url: str) -> None:
        """
        TODO
        """
        # вот сюда нужно передать объект конфигурации с этим урлом
        self.url = url

    def _get_candidates(self) -> list:
        """
        TODO
        """
        result = requests.get(f"{self.url}/candidates")
        if result.status_code == 200:
            result = result.json()
            return result

    def _get_candidates_skills(self) -> tuple:
        """
        TODO
        """
        # на такого размера кусках кода уже можно немного комментить
        results = []
        error_count = None
        candidates_names = self._get_candidates()
        # внимательней к названиям.
        for candidate_name in candidates_names:
            res = requests.get(f"{self.url}/candidates/{candidate_name}")
            if res.status_code == 200:
                candidate_data = res.json() # не удачная практика переиспользования переменнной. имён можно придумать оч много, отражающих смысл того, что в переменной сейчас находится.
                candidate_data__validated = self._validate_skills(candidate_data)
                if candidate_data__validated:
                    results.append(res)
                else:
                    error_count += 1
        return results, error_count

    def _validate_skills(self, data: dict) -> bool:
        """
        TODO
        """
        for name, property in data.items():
            try:
                float(property["skills"])
            except ValueError:
                return False
        return True

    def get_data(self) -> tuple:
        """
        TODO
        """
        result, errors = self._get_candidates_skills()
        return result, errors
