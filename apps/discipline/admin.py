from django.contrib import admin
from .models import Discipline

class DisciplineAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'user')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Discipline, DisciplineAdmin)
