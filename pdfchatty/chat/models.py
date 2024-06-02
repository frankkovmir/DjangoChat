from django.db import models
from django.utils import timezone

class ProcessedFile(models.Model):
    filename = models.CharField(max_length=255, unique=True)
    last_modified = models.DateTimeField(default=timezone.now)
