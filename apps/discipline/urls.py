from django.urls import path
from .views import DisciplineListAndCreate, DisciplineUpdateAndDelete

urlpatterns = [
    path('', DisciplineListAndCreate.as_view(), name='discipline-list-create'),
    path('<str:discipline_id>', DisciplineUpdateAndDelete.as_view(), name='discipline-update-delete'),
]
