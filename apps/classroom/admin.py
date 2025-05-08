from django.contrib import admin
from .models import Classroom

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Classroom, ClassroomAdmin)
