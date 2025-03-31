from django.urls import path
from .views import ClassroomListAndCreate, ClassroomUpdateAndDelete

urlpatterns = [
    path('', ClassroomListAndCreate.as_view(), name='classroom-list-create'),
    path('<str:classroom_id>', ClassroomUpdateAndDelete.as_view(), name='classroom-update-delete'),
]
