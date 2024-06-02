from django.contrib import admin
from chat.models import ChatSession, Message, ProcessedFile

admin.site.register(ChatSession)
admin.site.register(Message)
admin.site.register(ProcessedFile)