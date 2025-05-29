import json
import requests
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from apps.question.models import Question

class QuestionService:
    @staticmethod
    def get_question(description) -> str:
        api_base = config('AI_API_BASE')
        prompt = f"Generate a question based on the following description: {description}"
        try:
            response = requests.post(
                    f"{api_base}/api/ai/response/question",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"prompt": prompt})
                )    
            if response.status_code != 200:
                return Response(
                    {"error": f"AI API returned an error: {response.status_code}"},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            return response.json().get("response", {})    
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to connect to AI API: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )
    
    @staticmethod
    def create_question(serializer, request) -> str:
        description = serializer.validated_data['description']
        response_data = QuestionService.get_question(description)
        answer = response_data.get('answer')
        if isinstance(answer, str) and answer.isdigit():
                answer = int(answer)
        question = Question.objects.create(
            title=response_data.get('title', ''),
            options=response_data.get('options', []),
            answer=answer if isinstance(answer, int) else None,
            answer_text=response_data.get('answer', ''),
            type=response_data.get('type', ''),
            user=request.user,
            )
        question.was_generated_by_ai = True
        question.save()
        return question