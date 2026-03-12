"""
Vessels models — Vessel data cache and user Subscriptions
"""
from django.db import models
from django.conf import settings


class Vessel(models.Model):
    """
    Cached vessel data from AIS Hub API.
    MMSI (Maritime Mobile Service Identity) is the unique identifier.
    """
    VESSEL_TYPE_CHOICES = [
        ('Cargo', 'Cargo'),
        ('Tanker', 'Tanker'),
        ('Passenger', 'Passenger'),
        ('Fishing', 'Fishing'),
        ('Tug', 'Tug'),
        ('Military', 'Military'),
        ('Sailing', 'Sailing'),
        ('Pleasure', 'Pleasure Craft'),
        ('HSC', 'High Speed Craft'),
        ('Pilot', 'Pilot Vessel'),
        ('SAR', 'Search and Rescue'),
        ('Other', 'Other'),
    ]

    mmsi = models.CharField(max_length=9, unique=True, db_index=True, help_text='Maritime Mobile Service Identity')
    imo = models.CharField(max_length=10, blank=True, default='', db_index=True, help_text='IMO number')
    name = models.CharField(max_length=200, db_index=True)
    callsign = models.CharField(max_length=20, blank=True, default='')
    vessel_type = models.CharField(max_length=50, choices=VESSEL_TYPE_CHOICES, default='Other', db_index=True)
    flag = models.CharField(max_length=100, blank=True, default='', db_index=True)
    cargo = models.CharField(max_length=200, blank=True, default='', db_index=True)

    # Position data
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True, help_text='Speed Over Ground (knots)')
    course = models.FloatField(null=True, blank=True, help_text='Course Over Ground (degrees)')
    heading = models.IntegerField(null=True, blank=True, help_text='True heading (degrees)')
    nav_status = models.CharField(max_length=100, blank=True, default='', help_text='Navigation status')

    # Voyage data
    destination = models.CharField(max_length=200, blank=True, default='')
    eta = models.CharField(max_length=100, blank=True, default='', help_text='Estimated Time of Arrival')
    draught = models.FloatField(null=True, blank=True, help_text='Draught in meters')
    length = models.FloatField(null=True, blank=True, help_text='Ship length in meters')
    width = models.FloatField(null=True, blank=True, help_text='Ship width in meters')

    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Vessel'
        verbose_name_plural = 'Vessels'

    def __str__(self):
        return f"{self.name} (MMSI: {self.mmsi})"


class Subscription(models.Model):
    """
    User subscription to track a specific vessel.
    A user can subscribe to multiple vessels.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    vessel = models.ForeignKey(
        Vessel,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, default='', help_text='Optional user notes about this subscription')

    class Meta:
        unique_together = ('user', 'vessel')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.vessel.name}"


class VesselPosition(models.Model):
    """
    Historical position snapshot for voyage replay.
    Recorded each time vessel data is refreshed from AIS Hub API or demo data.
    """
    vessel = models.ForeignKey(
        Vessel,
        on_delete=models.CASCADE,
        related_name='positions'
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(null=True, blank=True, help_text='Speed Over Ground (knots)')
    course = models.FloatField(null=True, blank=True, help_text='Course Over Ground (degrees)')
    heading = models.IntegerField(null=True, blank=True, help_text='True heading (degrees)')
    nav_status = models.CharField(max_length=100, blank=True, default='')
    recorded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Vessel Position'
        verbose_name_plural = 'Vessel Positions'
        indexes = [
            models.Index(fields=['vessel', 'recorded_at']),
        ]

    def __str__(self):
        return f"{self.vessel.name} @ {self.recorded_at:%Y-%m-%d %H:%M}"
