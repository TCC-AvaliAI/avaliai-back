from django.urls import path
from apps.message.views import *

urlpatterns = [
    path('', MessageListAndCreateView.as_view(), name='message-list-create'),
    path('<str:message_id>/', MessageUpdateAndDeleteView.as_view(), name='message-update-delete'),
]
