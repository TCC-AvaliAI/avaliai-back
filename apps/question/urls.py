from django.urls import path
from .views import QuestionListAndCreate, QuestionUpdateAndDelete, CreateQuestionByAI

urlpatterns = [
    path('', QuestionListAndCreate.as_view(), name='question-list-create'),
    path('ai/', CreateQuestionByAI.as_view(), name='question-list-create-ai'),
    path('<str:question_id>', QuestionUpdateAndDelete.as_view(), name='question-update-delete'),
]
