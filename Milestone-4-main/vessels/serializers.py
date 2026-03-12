"""
Vessels serializers — Vessel list/detail, Subscription CRUD, Voyage Replay, and Dashboard analytics
"""
from rest_framework import serializers
from .models import Vessel, Subscription, VesselPosition


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


# ─── Voyage Replay Serializers ───────────────────────────────────────────────

class VesselPositionSerializer(serializers.ModelSerializer):
    """Serializer for historical vessel position snapshots."""
    vessel_name = serializers.CharField(source='vessel.name', read_only=True)
    vessel_mmsi = serializers.CharField(source='vessel.mmsi', read_only=True)

    class Meta:
        model = VesselPosition
        fields = [
            'id', 'vessel_mmsi', 'vessel_name',
            'latitude', 'longitude', 'speed', 'course',
            'heading', 'nav_status', 'recorded_at',
        ]
        read_only_fields = fields


# ─── Dashboard Serializers ───────────────────────────────────────────────────

class VesselTypeBreakdownSerializer(serializers.Serializer):
    """Breakdown of vessel count by type."""
    vessel_type = serializers.CharField()
    count = serializers.IntegerField()


class CompanyStatsSerializer(serializers.Serializer):
    """Company-level fleet statistics."""
    total_vessels = serializers.IntegerField()
    active_vessels = serializers.IntegerField(help_text='Vessels currently under way')
    moored_vessels = serializers.IntegerField()
    anchored_vessels = serializers.IntegerField()
    average_speed = serializers.FloatField(help_text='Average speed in knots (active vessels)')
    total_subscribers = serializers.IntegerField()
    vessel_type_breakdown = VesselTypeBreakdownSerializer(many=True)


class PortMetricSerializer(serializers.Serializer):
    """Metrics for a single destination port."""
    destination = serializers.CharField()
    vessel_count = serializers.IntegerField()
    avg_speed = serializers.FloatField(allow_null=True)
    vessel_types = serializers.ListField(child=serializers.CharField())


class PortMetricsSerializer(serializers.Serializer):
    """Aggregated port-level metrics."""
    total_destinations = serializers.IntegerField()
    top_ports = PortMetricSerializer(many=True)


class VesselRiskSerializer(serializers.Serializer):
    """Risk assessment for a single vessel."""
    mmsi = serializers.CharField()
    name = serializers.CharField()
    vessel_type = serializers.CharField()
    risk_score = serializers.FloatField(help_text='0-100 risk score')
    risk_factors = serializers.ListField(child=serializers.CharField())
    speed = serializers.FloatField(allow_null=True)
    nav_status = serializers.CharField()


class RiskDataSerializer(serializers.Serializer):
    """Insurer risk data aggregation."""
    total_assessed = serializers.IntegerField()
    high_risk_count = serializers.IntegerField()
    medium_risk_count = serializers.IntegerField()
    low_risk_count = serializers.IntegerField()
    average_risk_score = serializers.FloatField()
    risk_by_type = serializers.DictField(child=serializers.FloatField())
    high_risk_vessels = VesselRiskSerializer(many=True)
