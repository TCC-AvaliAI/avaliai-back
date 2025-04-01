from django.urls import path
from .views import QuestionListAndCreate, QuestionUpdateAndDelete

urlpatterns = [
    path('', QuestionListAndCreate.as_view(), name='question-list-create'),
    path('<str:question_id>', QuestionUpdateAndDelete.as_view(), name='question-update-delete'),
]
