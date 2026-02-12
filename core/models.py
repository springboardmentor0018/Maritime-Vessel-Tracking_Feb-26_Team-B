
# Create your models here.
from django.db import models

class Vessel(models.Model):
    imo_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    vessel_type = models.CharField(max_length=50)
    flag = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Port(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    congestion_score = models.FloatField(default=0)

    def __str__(self):
        return self.name

        