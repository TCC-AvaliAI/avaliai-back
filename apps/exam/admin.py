from django.contrib import admin

class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    search_fields = ('name',)
    ordering = ('id',)
