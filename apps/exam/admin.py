from django.contrib import admin
from .models import Exam

class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'theme', 'created_at', 'status', 'was_generated_by_ai')
    search_fields = ('name',)
    ordering = ('title',)

admin.site.register(Exam, ExamAdmin)
