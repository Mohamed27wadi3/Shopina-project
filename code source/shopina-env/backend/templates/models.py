from django.db import models

class Template(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    image = models.URLField(max_length=500)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
