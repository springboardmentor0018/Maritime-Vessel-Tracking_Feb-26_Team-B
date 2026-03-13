"""
Vessels views — List, Search, Detail, Refresh, and Subscription management
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .models import Vessel, Subscription
from .serializers import (
    VesselListSerializer,
    VesselDetailSerializer,
    SubscriptionSerializer,
    CreateSubscriptionSerializer,
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
