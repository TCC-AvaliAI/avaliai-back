from django.contrib import admin

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    search_fields = ('name',)
    ordering = ('id',)
