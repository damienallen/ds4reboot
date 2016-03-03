from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# Create your models here.

class Turf(models.Model):

    turf_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    turf_to = models.CharField(max_length=30)
    turf_by = models.CharField(max_length=30)

    turf_time = models.DateTimeField(default=timezone.now)

    turf_count = models.DecimalField(decimal_places=2, max_digits=5)
    turf_type = models.CharField(max_length=10)



class Boete(models.Model):

    boete_user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_by = models.CharField(max_length=30)
    created_time = models.DateTimeField(default=timezone.now)

    boete_value = models.IntegerField(default=1)
    boete_note = models.CharField(max_length=50)