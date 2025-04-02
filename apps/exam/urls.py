from django.urls import path
from .views import ExamListAndCreate, ExamUpdateAndDelete, ExamQuestions, CreateExamByAI

urlpatterns = [
    path('', ExamListAndCreate.as_view(), name='exam-list-create'),
    path('ai/', CreateExamByAI.as_view(), name='exam-create-ai'),
    path('<str:exam_id>', ExamUpdateAndDelete.as_view(), name='exam-update-delete'),
    path('<str:exam_id>/questions/', ExamQuestions.as_view(), name='exam-list-add-question'),
]
