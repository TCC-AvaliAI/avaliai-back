from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    search_fields = ('name',)
    ordering = ('id',)

admin.site.register(Question, QuestionAdmin)
