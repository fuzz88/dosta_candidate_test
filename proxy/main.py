# python 3.9

from fastapi import FastAPI, responses, exceptions
from pydantic import BaseModel, ValidationError, validator
import uvicorn
import httpx

app = FastAPI()
ORIGINAL_HOST = 'http://localhost:8089/'


class Candidate(BaseModel):
    skills: float
    tools: list

    @validator('tools')
    def check_tools(cls, v):
        for row in v:
            if not isinstance(row, str):
                raise TypeError('value is not a valid string')
        return v


@app.get("/")
def home():
    return {"Main page - healthcheck"}


@app.get("/candidates")
def candidates():
    # Получаем список всех кандидатов
    response = httpx.get(f'{ORIGINAL_HOST}candidates')
    if response.reason_phrase != 'OK':
        raise exceptions.HTTPException(response.status_code)
    candidates = response.json()
    if candidates is None or not isinstance(candidates, list):
        raise exceptions.HTTPException(404)

    # Получаем параметры каждого кандидата
    if candidates:
        result, errors = {}, {}
        for candidate in candidates:
            response = httpx.get(f'{ORIGINAL_HOST}candidates/{candidate}')
            if response.reason_phrase == 'OK':
                try:
                    candidate_json = response.json()
                    candidate_params = candidate_json[candidate]

                    # Валидируем данные кандидата
                    Candidate.parse_obj(candidate_params)
                    result[candidate] = candidate_params
                except ValidationError as e:
                    errors[candidate] = e.errors()
            else:
                errors[candidate] = 'Not found'

        # Если есть ошибки валидации возвращаем 206 и список валидных кандидатов
        if errors:
            result['errors'] = errors
            return responses.JSONResponse(content=result, status_code=206)
        else:
            return responses.JSONResponse(content=result, status_code=200)
    else:
        exceptions.HTTPException(404)


if __name__ == '__main__':
    uvicorn.run("main:app", port=9999, host="0.0.0.0", reload=True)
