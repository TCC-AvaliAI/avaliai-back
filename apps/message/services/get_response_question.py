import json
import requests
from decouple import config

class ResponseQuestionService:
    @staticmethod
    def get_question_response(prompt: str) -> str:
        api_base = config('AI_API_BASE')
        response = requests.post(
            f"{api_base}/api/ai/response",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"prompt": prompt})
        )
        return response.json().get('answer', 'Desculpe, não consegui encontrar uma resposta para sua pergunta.')