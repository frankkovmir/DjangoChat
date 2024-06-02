from django.db import models
from django.utils import timezone
class ChatSession(models.Model):
    session_key = models.CharField(max_length=255, unique=True)

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10)
    message_type = models.CharField(max_length=10)
    text_content = models.TextField(null=True, blank=True)
    blob_content = models.BinaryField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class ProcessedFile(models.Model):
    filename = models.CharField(max_length=255, unique=True)
    last_modified = models.DateTimeField(default=timezone.now)