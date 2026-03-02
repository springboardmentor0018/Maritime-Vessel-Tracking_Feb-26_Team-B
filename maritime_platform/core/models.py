from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# -------------------------
# Vessel Model
# -------------------------
class Vessel(models.Model):
    imo_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    vessel_type = models.CharField(max_length=50)
    cargo_type = models.CharField(max_length=50)
    operator = models.CharField(max_length=100)
    last_position_lat = models.FloatField()
    last_position_lon = models.FloatField()
    speed = models.FloatField(null=True, blank=True)
    heading = models.FloatField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# -------------------------
# Port Model (Week 3 Task)
# -------------------------
class Port(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    congestion_score = models.FloatField(help_text="0–10 congestion scale")
    avg_wait_time = models.FloatField(help_text="Average wait time in hours")
    arrivals = models.IntegerField()
    departures = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.country}"


# -------------------------
# Voyage Model
# -------------------------
class Voyage(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    port_from = models.ForeignKey(
        Port,
        related_name='departures_from',
        on_delete=models.CASCADE
    )
    port_to = models.ForeignKey(
        Port,
        related_name='arrivals_to',
        on_delete=models.CASCADE
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vessel.name}: {self.port_from} → {self.port_to}"


# -------------------------
# Event Model
# -------------------------
class Event(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField()

    def __str__(self):
        return self.event_type


# -------------------------
# Notification Model (Week 3 Task)
# -------------------------
class Notification(models.Model):
    ALERT_TYPES = [
        ('congestion', 'Port Congestion'),
        ('weather', 'Weather Alert'),
        ('safety', 'Safety Alert'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPES,
        default='congestion'
    )
    port = models.ForeignKey(
        Port,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.alert_type} alert for {self.user.username}"


# -------------------------
# User Profile Model
# -------------------------
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('OPERATOR', 'Operator'),
        ('ANALYST', 'Analyst'),
        ('ADMIN', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


# -------------------------
# Subscription Model
# -------------------------
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    alert_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} → {self.vessel.name}"