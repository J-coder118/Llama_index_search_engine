from django.db import models

# Create your models here.

class Document(models.Model):
    file = models.FileField(upload_to='pdf_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Pinecone_indice(models.Model):
    path = models.TextField()
    pinecone_title = models.TextField()
    # GPTVector = models.JSONField()
    # idx_summaries = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)