import json
import requests
from decouple import config

class ResponseQuestionService:
    @staticmethod
    def get_question_response(question: str) -> str:
        api_base = config('AI_API_BASE')
        response = requests.post(
            f"{api_base}/api/ai/response/question",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"question": question})
        )
        return response.json().get('answer', 'Desculpe, não consegui encontrar uma resposta para sua pergunta.')