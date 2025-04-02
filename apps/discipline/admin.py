from django.contrib import admin
from .models import Discipline

class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    search_fields = ('name',)
    ordering = ('id',)

admin.site.register(Discipline, DisciplineAdmin)
