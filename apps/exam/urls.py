from django.urls import path
from .views import ExamListAndCreate, ExamDetailUpdateAndDelete, ExamQuestions, CreateExamByAI, ExamDetails, UpdateExamQRCode

urlpatterns = [
    path('', ExamListAndCreate.as_view(), name='exam-list-create'),
    path('ai/', CreateExamByAI.as_view(), name='exam-create-ai'),
    path('<str:exam_id>', ExamDetailUpdateAndDelete.as_view(), name='exam-update-delete'),
    path('<str:exam_id>/questions/', ExamQuestions.as_view(), name='exam-list-add-question'),
    path('details/', ExamDetails.as_view(), name='exam-details'),
    path('<str:exam_id>/qrcode/', UpdateExamQRCode.as_view(), name='exam-update-qr-code'),
]
