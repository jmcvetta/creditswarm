from django.db import models
from django.contrib.auth.models import User

# Create your models here.

BUREAUS = [
    ('experian', 'Experian'),
    ('equifax', 'Equifax'),
    ('transunion', 'TransUnion'),
    ]

class Complaint(models.Model):
    user = models.ForeignKey(User, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False)
    bureau = models.CharField(max_length=32, choices=BUREAUS, blank=False)
    body = models.TextField(blank=False)