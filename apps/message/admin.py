from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('role', 'content', 'timestamp')
    search_fields = ('content',)
    ordering = ('id',)

admin.site.register(Message, MessageAdmin)
