import json
import requests
from decouple import config

class ResponseQuestionService:
    @staticmethod
    def get_question_response(prompt: str, model: str, api_key: str) -> str:
        api_base = config('AI_API_BASE')
        data = {
            "prompt": prompt,
            "model": model,
            "api_key": api_key
        }
        response = requests.post(
            f"{api_base}/api/ai/response",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        print(response.text)
        return response.json().get('answer', 'Desculpe, não consegui encontrar uma resposta para sua pergunta.')