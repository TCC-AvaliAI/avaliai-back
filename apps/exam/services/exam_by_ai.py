import json
import requests
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from apps.question.models import Question


class ExamService:
    @staticmethod
    def create_exam_by_ai(serializer, prompt, user):
        api_base = config('AI_API_BASE')
        response = requests.post(
                    f"{api_base}/api/ai/response/",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"prompt": prompt})
                )
        response_data = response.json()
        exam = serializer.save(was_generated_by_ai=True)
        for question_data in response_data["response"]:
            answer = question_data['answer']
            if isinstance(answer, str) and answer.isdigit():
                answer = int(answer)
            question = Question.objects.create(
                title=question_data['title'],
                options=question_data['options'],
                answer=answer if isinstance(answer, int) else None,
                answer_text=question_data['answer'],
                type=question_data['type'],
                user=user,
            )
            question.save()
            exam.questions.add(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)