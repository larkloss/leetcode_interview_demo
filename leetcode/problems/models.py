from django.db import models
from django.conf import settings

# Create your models here.
class Problem(models.Model):
    url = models.URLField()
    company = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    
class Mock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey('problems.Problem', related_name='mocks', on_delete=models.CASCADE)