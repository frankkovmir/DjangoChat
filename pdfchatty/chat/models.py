from django.db import models

class ChatSession(models.Model):
    session_key = models.CharField(max_length=255, unique=True)

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10)
    message_type = models.CharField(max_length=10)
    text_content = models.TextField(null=True, blank=True)
    blob_content = models.BinaryField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)