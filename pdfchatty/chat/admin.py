from django.contrib import admin
from chat.models import ChatSession, Message

admin.site.register(ChatSession)
admin.site.register(Message)