"""
Vessels views — List, Search, Detail, Refresh, Subscription management,
                 Voyage Replay, and Dashboard analytics
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Avg, F, Value
from django.db.models.functions import Coalesce
from django.utils.dateparse import parse_datetime

from .models import Vessel, Subscription, VesselPosition
from .serializers import (
    VesselListSerializer,
    VesselDetailSerializer,
    SubscriptionSerializer,
    CreateSubscriptionSerializer,
    VesselPositionSerializer,
    CompanyStatsSerializer,
    PortMetricsSerializer,
    RiskDataSerializer,
)
from .services import AISHubService


class VesselPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ─── Vessel Endpoints ────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vessel_list(request):
    """
    List all vessels with pagination.

    GET /api/vessels/
    Query params: page, page_size
    """
    # Ensure demo data is loaded if DB is empty
    if not Vessel.objects.exists():
        service = AISHubService()
        service.fetch_vessels()

    vessels = Vessel.objects.all()
    paginator = VesselPagination()
    page = paginator.paginate_queryset(vessels, request)
    serializer = VesselListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vessel_search(request):
    """
    Search and filter vessels by type, flag, cargo, or name.

    GET /api/vessels/search/?name=ever&type=Cargo&flag=Panama&cargo=Container
    All query params are optional and combined with AND logic.
    """
    # Ensure demo data is loaded
    if not Vessel.objects.exists():
        service = AISHubService()
        service.fetch_vessels()

    queryset = Vessel.objects.all()

    # Apply filters
    name = request.query_params.get('name', '').strip()
    vessel_type = request.query_params.get('type', '').strip()
    flag = request.query_params.get('flag', '').strip()
    cargo = request.query_params.get('cargo', '').strip()
    query = request.query_params.get('q', '').strip()

    if name:
        queryset = queryset.filter(name__icontains=name)
    if vessel_type:
        queryset = queryset.filter(vessel_type__icontains=vessel_type)
    if flag:
        queryset = queryset.filter(flag__icontains=flag)
    if cargo:
        queryset = queryset.filter(cargo__icontains=cargo)
    if query:
        # General search across multiple fields
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(mmsi__icontains=query) |
            Q(imo__icontains=query) |
            Q(flag__icontains=query) |
            Q(cargo__icontains=query) |
            Q(destination__icontains=query) |
            Q(callsign__icontains=query)
        )

    paginator = VesselPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = VesselListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vessel_detail(request, mmsi):
    """
    Get full details of a specific vessel by MMSI.

    GET /api/vessels/<mmsi>/
    """
    service = AISHubService()
    vessel = service.get_vessel_by_mmsi(mmsi)

    if not vessel:
        return Response({
            'success': False,
            'message': f'Vessel with MMSI {mmsi} not found.',
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = VesselDetailSerializer(vessel)

    # Check if user is subscribed
    is_subscribed = Subscription.objects.filter(
        user=request.user, vessel=vessel
    ).exists()

    data = serializer.data
    data['is_subscribed'] = is_subscribed

    return Response({
        'success': True,
        'data': data,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vessel_refresh(request):
    """
    Force refresh vessel data from AIS Hub API.

    POST /api/vessels/refresh/
    """
    service = AISHubService()
    vessels = service.fetch_vessels()

    return Response({
        'success': True,
        'message': f'Vessel data refreshed. {vessels.count()} vessels in database.',
        'demo_mode': service.is_demo_mode,
    }, status=status.HTTP_200_OK)


# ─── Subscription Endpoints ──────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def subscription_list_create(request):
    """
    GET  /api/subscriptions/ — List user's subscriptions
    POST /api/subscriptions/ — Subscribe to a vessel (body: { vessel_mmsi, notes? })
    """
    if request.method == 'GET':
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response({
            'success': True,
            'count': subscriptions.count(),
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    # POST — Create subscription
    serializer = CreateSubscriptionSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)

    subscription = Subscription.objects.create(
        user=request.user,
        vessel=serializer.validated_data['vessel'],
        notes=serializer.validated_data.get('notes', ''),
    )

    return Response({
        'success': True,
        'message': f'Subscribed to {subscription.vessel.name}.',
        'data': SubscriptionSerializer(subscription).data,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscription_detail(request, pk):
    """
    GET    /api/subscriptions/<id>/ — View subscription detail
    DELETE /api/subscriptions/<id>/ — Unsubscribe
    """
    try:
        subscription = Subscription.objects.get(pk=pk, user=request.user)
    except Subscription.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Subscription not found.',
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscription)
        return Response({
            'success': True,
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    # DELETE
    vessel_name = subscription.vessel.name
    subscription.delete()

    return Response({
        'success': True,
        'message': f'Unsubscribed from {vessel_name}.',
    }, status=status.HTTP_200_OK)


# ─── Voyage Replay Endpoints ─────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def voyage_replay(request, mmsi):
    """
    Fetch historical positions for a vessel for voyage replay / playback.

    GET /api/vessels/<mmsi>/replay/
    Query params:
        start   — ISO datetime string, filter positions after this time
        end     — ISO datetime string, filter positions before this time
        limit   — max positions to return (default 200, max 1000)
    """
    try:
        vessel = Vessel.objects.get(mmsi=mmsi)
    except Vessel.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Vessel with MMSI {mmsi} not found.',
        }, status=status.HTTP_404_NOT_FOUND)

    queryset = VesselPosition.objects.filter(vessel=vessel)

    # Apply time range filters
    start = request.query_params.get('start')
    end = request.query_params.get('end')

    if start:
        start_dt = parse_datetime(start)
        if start_dt:
            queryset = queryset.filter(recorded_at__gte=start_dt)

    if end:
        end_dt = parse_datetime(end)
        if end_dt:
            queryset = queryset.filter(recorded_at__lte=end_dt)

    limit = min(int(request.query_params.get('limit', 200)), 1000)

    # Order chronologically for replay playback
    positions = queryset.order_by('recorded_at')[:limit]
    serializer = VesselPositionSerializer(positions, many=True)

    return Response({
        'success': True,
        'vessel': {
            'mmsi': vessel.mmsi,
            'name': vessel.name,
            'vessel_type': vessel.vessel_type,
        },
        'count': len(serializer.data),
        'data': serializer.data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def voyage_replay_latest(request, mmsi):
    """
    Fetch the N most recent positions for quick replay preview.

    GET /api/vessels/<mmsi>/replay/latest/
    Query params:
        count — number of recent positions (default 50, max 200)
    """
    try:
        vessel = Vessel.objects.get(mmsi=mmsi)
    except Vessel.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Vessel with MMSI {mmsi} not found.',
        }, status=status.HTTP_404_NOT_FOUND)

    count = min(int(request.query_params.get('count', 50)), 200)

    # Get latest N positions, then reverse for chronological order
    positions = list(
        VesselPosition.objects.filter(vessel=vessel).order_by('-recorded_at')[:count]
    )
    positions.reverse()

    serializer = VesselPositionSerializer(positions, many=True)

    return Response({
        'success': True,
        'vessel': {
            'mmsi': vessel.mmsi,
            'name': vessel.name,
            'vessel_type': vessel.vessel_type,
        },
        'count': len(serializer.data),
        'data': serializer.data,
    }, status=status.HTTP_200_OK)


# ─── Dashboard Endpoints ─────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_company_stats(request):
    """
    Company fleet statistics.

    GET /api/dashboard/company-stats/
    Returns: total vessels, active/moored/anchored counts, avg speed, type breakdown.
    """
    # Ensure data exists
    if not Vessel.objects.exists():
        service = AISHubService()
        service.fetch_vessels()

    vessels = Vessel.objects.all()
    total = vessels.count()

    # Navigation status classification
    active_statuses = ['Under way using engine', 'Under sail']
    moored_statuses = ['Moored']
    anchored_statuses = ['At anchor']

    active_vessels = vessels.filter(nav_status__in=active_statuses).count()
    moored_vessels = vessels.filter(nav_status__in=moored_statuses).count()
    anchored_vessels = vessels.filter(nav_status__in=anchored_statuses).count()

    # Average speed of active vessels
    avg_speed_result = vessels.filter(
        nav_status__in=active_statuses, speed__isnull=False
    ).aggregate(avg_speed=Avg('speed'))
    avg_speed = round(avg_speed_result['avg_speed'] or 0, 2)

    # Vessel type breakdown
    type_breakdown = (
        vessels.values('vessel_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Total subscribers across all vessels
    total_subscribers = Subscription.objects.count()

    stats = {
        'total_vessels': total,
        'active_vessels': active_vessels,
        'moored_vessels': moored_vessels,
        'anchored_vessels': anchored_vessels,
        'average_speed': avg_speed,
        'total_subscribers': total_subscribers,
        'vessel_type_breakdown': list(type_breakdown),
    }

    serializer = CompanyStatsSerializer(stats)
    return Response({
        'success': True,
        'data': serializer.data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_port_metrics(request):
    """
    Port/destination analytics.

    GET /api/dashboard/port-metrics/
    Returns: top destinations by vessel count, avg speed per port, vessel types per port.
    """
    if not Vessel.objects.exists():
        service = AISHubService()
        service.fetch_vessels()

    vessels = Vessel.objects.exclude(destination='').exclude(destination__isnull=True)

    # Group by destination
    destinations = (
        vessels.values('destination')
        .annotate(vessel_count=Count('id'), avg_speed=Avg('speed'))
        .order_by('-vessel_count')[:20]
    )

    top_ports = []
    for dest in destinations:
        port_vessels = vessels.filter(destination=dest['destination'])
        vessel_types = list(
            port_vessels.values_list('vessel_type', flat=True).distinct()
        )
        top_ports.append({
            'destination': dest['destination'],
            'vessel_count': dest['vessel_count'],
            'avg_speed': round(dest['avg_speed'] or 0, 2),
            'vessel_types': vessel_types,
        })

    total_destinations = (
        vessels.values('destination').distinct().count()
    )

    data = {
        'total_destinations': total_destinations,
        'top_ports': top_ports,
    }

    serializer = PortMetricsSerializer(data)
    return Response({
        'success': True,
        'data': serializer.data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_risk_data(request):
    """
    Insurer risk assessment data.

    GET /api/dashboard/risk-data/
    Returns: per-vessel risk scores based on speed, nav status, and vessel type.
    Risk factors:
      - High speed (>15 kn)           → +30 points
      - Dangerous nav status           → +25 points
      - Large vessel (>300m)           → +15 points
      - Tanker carrying hazardous cargo → +20 points
      - No destination set             → +10 points
    """
    if not Vessel.objects.exists():
        service = AISHubService()
        service.fetch_vessels()

    vessels = Vessel.objects.all()
    dangerous_statuses = [
        'Not under command', 'Restricted manoeuvrability',
        'Constrained by her draught', 'Aground',
    ]

    risk_assessments = []
    for vessel in vessels:
        risk_score = 0.0
        factors = []

        # Speed risk
        if vessel.speed and vessel.speed > 15:
            risk_score += 30
            factors.append(f'High speed: {vessel.speed} kn')
        elif vessel.speed and vessel.speed > 10:
            risk_score += 10
            factors.append(f'Moderate speed: {vessel.speed} kn')

        # Navigation status risk
        if vessel.nav_status in dangerous_statuses:
            risk_score += 25
            factors.append(f'Dangerous nav status: {vessel.nav_status}')

        # Size risk
        if vessel.length and vessel.length > 300:
            risk_score += 15
            factors.append(f'Large vessel: {vessel.length}m length')

        # Cargo risk (tankers with hazardous cargo)
        hazardous_cargos = ['Crude Oil', 'LNG', 'Petroleum Products', 'Chemicals']
        if vessel.vessel_type == 'Tanker' and vessel.cargo in hazardous_cargos:
            risk_score += 20
            factors.append(f'Hazardous cargo: {vessel.cargo}')

        # Missing destination
        if not vessel.destination:
            risk_score += 10
            factors.append('No destination set')

        # Cap at 100
        risk_score = min(risk_score, 100)

        risk_assessments.append({
            'mmsi': vessel.mmsi,
            'name': vessel.name,
            'vessel_type': vessel.vessel_type,
            'risk_score': risk_score,
            'risk_factors': factors,
            'speed': vessel.speed,
            'nav_status': vessel.nav_status,
        })

    # Classify by risk level
    high_risk = [r for r in risk_assessments if r['risk_score'] >= 50]
    medium_risk = [r for r in risk_assessments if 25 <= r['risk_score'] < 50]
    low_risk = [r for r in risk_assessments if r['risk_score'] < 25]

    # Average risk score by vessel type
    risk_by_type = {}
    for r in risk_assessments:
        vtype = r['vessel_type']
        if vtype not in risk_by_type:
            risk_by_type[vtype] = []
        risk_by_type[vtype].append(r['risk_score'])

    avg_risk_by_type = {
        vtype: round(sum(scores) / len(scores), 2)
        for vtype, scores in risk_by_type.items()
    }

    total_score = sum(r['risk_score'] for r in risk_assessments)
    avg_risk = round(total_score / len(risk_assessments), 2) if risk_assessments else 0

    data = {
        'total_assessed': len(risk_assessments),
        'high_risk_count': len(high_risk),
        'medium_risk_count': len(medium_risk),
        'low_risk_count': len(low_risk),
        'average_risk_score': avg_risk,
        'risk_by_type': avg_risk_by_type,
        'high_risk_vessels': sorted(high_risk, key=lambda x: x['risk_score'], reverse=True),
    }

    serializer = RiskDataSerializer(data)
    return Response({
        'success': True,
        'data': serializer.data,
    }, status=status.HTTP_200_OK)
