from django.urls import path
from .views import QuestionListAndCreate, QuestionUpdateAndDelete, CreateQuestionByAI, RecentQuestions

urlpatterns = [
    path('', QuestionListAndCreate.as_view(), name='question-list-create'),
    path('ai/', CreateQuestionByAI.as_view(), name='question-list-create-ai'),
    path('recents/', RecentQuestions.as_view(), name='recent-questions'),
    path('<str:question_id>', QuestionUpdateAndDelete.as_view(), name='question-update-delete'),
]
