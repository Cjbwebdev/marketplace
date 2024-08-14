from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(default=0.00)  # Ensure a default value is set
    image = models.ImageField(upload_to='items/')
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE)
    available_dates = models.TextField(blank=True, null=True)
    daily_price = models.FloatField(default=0.00)

    def __str__(self):
        return self.name
