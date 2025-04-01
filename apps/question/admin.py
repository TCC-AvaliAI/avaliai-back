from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    search_fields = ('name',)
    ordering = ('id',)
