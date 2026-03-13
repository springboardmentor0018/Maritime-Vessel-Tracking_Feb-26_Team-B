"""
Vessels serializers — Vessel list/detail and Subscription CRUD
"""
from rest_framework import serializers
from .models import Vessel, Subscription


class VesselListSerializer(serializers.ModelSerializer):
    """Compact vessel representation for list views."""
    class Meta:
        model = Vessel
        fields = [
            'mmsi', 'imo', 'name', 'vessel_type', 'flag',
            'cargo', 'latitude', 'longitude', 'speed',
            'nav_status', 'last_updated',
        ]


class VesselDetailSerializer(serializers.ModelSerializer):
    """Full vessel details including dimensions and voyage info."""
    subscriber_count = serializers.SerializerMethodField()

    class Meta:
        model = Vessel
        fields = '__all__'

    def get_subscriber_count(self, obj):
        return obj.subscribers.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Subscription with nested vessel details."""
    vessel = VesselListSerializer(read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user_email', 'vessel', 'notes', 'created_at']
        read_only_fields = ['id', 'user_email', 'created_at']


class CreateSubscriptionSerializer(serializers.Serializer):
    """Create a subscription by vessel MMSI."""
    vessel_mmsi = serializers.CharField(max_length=9)
    notes = serializers.CharField(required=False, default='', allow_blank=True)

    def validate_vessel_mmsi(self, value):
        try:
            Vessel.objects.get(mmsi=value)
        except Vessel.DoesNotExist:
            raise serializers.ValidationError(
                f'No vessel found with MMSI {value}. Try refreshing vessel data first.'
            )
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        vessel = Vessel.objects.get(mmsi=attrs['vessel_mmsi'])

        if Subscription.objects.filter(user=user, vessel=vessel).exists():
            raise serializers.ValidationError(
                {'vessel_mmsi': 'You are already subscribed to this vessel.'}
            )

        attrs['vessel'] = vessel
        return attrs
from .models import Port, Notification


class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'