from django.urls import path
from .views import QuestionListAndCreate, QuestionUpdateAndDelete, CreateQuestionByAI, RecentQuestions, QuestionListAndAddTags

urlpatterns = [
    path('', QuestionListAndCreate.as_view(), name='question-list-create'),
    path('ai/', CreateQuestionByAI.as_view(), name='question-list-create-ai'),
    path('recents/', RecentQuestions.as_view(), name='recent-questions'),
    path('<str:question_id>', QuestionUpdateAndDelete.as_view(), name='question-update-delete'),
    path('<str:question_id>/tags/', QuestionListAndAddTags.as_view(), name='list-question-add-tags'),
]
