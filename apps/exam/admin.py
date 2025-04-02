from django.contrib import admin
from .models import Exam

class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    search_fields = ('name',)
    ordering = ('id',)

admin.site.register(Exam, ExamAdmin)
