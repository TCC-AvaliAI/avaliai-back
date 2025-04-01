from django.urls import path
from .views import ExamListAndCreate, ExamUpdateAndDelete

urlpatterns = [
    path('', ExamListAndCreate.as_view(), name='exam-list-create'),
    path('<str:exam_id>', ExamUpdateAndDelete.as_view(), name='exam-update-delete'),
]
