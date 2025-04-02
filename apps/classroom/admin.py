from django.contrib import admin
from .models import Classroom

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    search_fields = ('name',)
    ordering = ('id',)

admin.site.register(Classroom, ClassroomAdmin)
