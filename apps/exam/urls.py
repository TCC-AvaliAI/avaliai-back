from django.urls import path
from apps.exam.views import *

urlpatterns = [
    path('', ExamListAndCreate.as_view(), name='exam-list-create'),
    path('ai/', CreateExamByAI.as_view(), name='exam-create-ai'),
    path('<str:exam_id>', ExamDetailUpdateAndDelete.as_view(), name='exam-update-delete'),
    path('<str:exam_id>/questions/', ExamQuestions.as_view(), name='exam-list-add-question'),
    path('details/', ExamDetails.as_view(), name='exam-details'),
    path('<str:exam_id>/qrcode/', UpdateExamQRCode.as_view(), name='exam-update-qr-code'),
    path('<str:exam_id>/file/', ExamPDFFile.as_view(), name='exam-pdf-file'),
    path('<str:exam_id>/apply/', MarkExamAsApplied.as_view(), name='exam-apply'),
    path('<str:exam_id>/archive/', MarkExamAsArchived.as_view(), name='exam-archive'),
    path('<str:exam_id>/cancel/', MarkExamAsCanceled.as_view(), name='exam-canceled'),
]
