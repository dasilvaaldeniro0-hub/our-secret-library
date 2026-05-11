from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=100, blank=True)

    cover_url = models.URLField()
    pdf_url = models.URLField()
    audio_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title