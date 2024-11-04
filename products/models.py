from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField()
    is_active = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title