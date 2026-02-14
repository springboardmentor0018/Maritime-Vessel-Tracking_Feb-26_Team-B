from django.db import models
from django.contrib.auth.models import User


class Vessel(models.Model):
    imo_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    vessel_type = models.CharField(max_length=50)
    cargo_type = models.CharField(max_length=50)
    operator = models.CharField(max_length=100)
    last_position_lat = models.FloatField()
    last_position_lon = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Port(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    congestion_score = models.FloatField()
    avg_wait_time = models.FloatField()
    arrivals = models.IntegerField()
    departures = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Voyage(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    port_from = models.ForeignKey(Port, related_name='departures_from', on_delete=models.CASCADE)
    port_to = models.ForeignKey(Port, related_name='arrivals_to', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vessel.name} voyage"


class Event(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    details = models.TextField()

    def __str__(self):
        return self.event_type


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.type

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('OPERATOR', 'Operator'),
        ('ANALYST', 'Analyst'),
        ('ADMIN', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username