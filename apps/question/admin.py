from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'answer', 'answer_text')
    search_fields = ('name',)
    ordering = ('id',)

admin.site.register(Question, QuestionAdmin)
