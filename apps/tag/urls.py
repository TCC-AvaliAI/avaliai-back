from django.urls import path
from apps.tag.views import *

urlpatterns = [
    path('', TagListAndCreateView.as_view(), name='tag-list-create'),
    path('<str:tag_id>', TagDetailUpdateAndDeleteView.as_view(), name='tag-detail-update-delete'),
]
