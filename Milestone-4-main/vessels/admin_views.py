"""
Admin API views — Health check, Logs, and Data Export (CSV)
All endpoints require IsAdminUser permission.
"""
import csv
import logging
from io import StringIO
from collections import deque

from django.http import HttpResponse
from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Vessel, Subscription, VesselPosition
from accounts.models import CustomUser

logger = logging.getLogger(__name__)


# ─── In-Memory Log Buffer ────────────────────────────────────────────────────
# Ring buffer to capture recent log entries for the admin logs endpoint.

class LogBufferHandler(logging.Handler):
    """Custom logging handler that stores log records in a ring buffer."""
    _buffer = deque(maxlen=500)

    def emit(self, record):
        try:
            log_entry = {
                'timestamp': self.format(record).split(' - ')[0] if ' - ' in self.format(record) else str(timezone.now()),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
            }
            LogBufferHandler._buffer.append(log_entry)
        except Exception:
            self.handleError(record)

    @classmethod
    def get_logs(cls, count=100):
        """Retrieve the most recent log entries."""
        logs = list(cls._buffer)
        return logs[-count:] if count < len(logs) else logs


# Install the log buffer handler on the root logger
_buffer_handler = LogBufferHandler()
_buffer_handler.setLevel(logging.DEBUG)
_buffer_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger('').addHandler(_buffer_handler)


# ─── Health Check ─────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_health(request):
    """
    GET /api/admin-api/health/
    Returns system health: DB status, vessel count, last update, demo mode, user count.
    """
    from django.conf import settings

    # Check database connectivity
    db_status = 'healthy'
    try:
        connection.ensure_connection()
    except Exception as e:
        db_status = f'error: {str(e)}'

    # Gather statistics
    vessel_count = Vessel.objects.count()
    user_count = CustomUser.objects.count()
    subscription_count = Subscription.objects.count()
    position_count = VesselPosition.objects.count()

    last_vessel_update = Vessel.objects.order_by('-last_updated').values_list(
        'last_updated', flat=True
    ).first()

    is_demo_mode = not bool(getattr(settings, 'AIS_API_KEY', ''))

    return Response({
        'success': True,
        'data': {
            'status': 'operational' if db_status == 'healthy' else 'degraded',
            'timestamp': timezone.now().isoformat(),
            'database': db_status,
            'demo_mode': is_demo_mode,
            'debug_mode': settings.DEBUG,
            'counts': {
                'vessels': vessel_count,
                'users': user_count,
                'subscriptions': subscription_count,
                'position_snapshots': position_count,
            },
            'last_vessel_update': last_vessel_update.isoformat() if last_vessel_update else None,
        }
    }, status=status.HTTP_200_OK)


# ─── Application Logs ────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_logs(request):
    """
    GET /api/admin-api/logs/?count=100&level=ERROR
    Returns recent application log entries from the in-memory ring buffer.
    """
    count = min(int(request.query_params.get('count', 100)), 500)
    level_filter = request.query_params.get('level', '').upper()

    logs = LogBufferHandler.get_logs(count=500)  # Get all, then filter

    if level_filter and level_filter in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
        level_priority = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}
        min_level = level_priority.get(level_filter, 0)
        logs = [l for l in logs if level_priority.get(l['level'], 0) >= min_level]

    logs = logs[-count:]

    return Response({
        'success': True,
        'count': len(logs),
        'data': logs,
    }, status=status.HTTP_200_OK)


# ─── CSV Export: Vessels ──────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_vessels_csv(request):
    """
    GET /api/admin-api/export/vessels/
    Downloads all vessel data as a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="vessels_export_{timezone.now():%Y%m%d_%H%M%S}.csv"'

    writer = csv.writer(response)
    # Header row
    writer.writerow([
        'MMSI', 'IMO', 'Name', 'Callsign', 'Type', 'Flag', 'Cargo',
        'Latitude', 'Longitude', 'Speed (kn)', 'Course', 'Heading',
        'Nav Status', 'Destination', 'ETA', 'Draught (m)',
        'Length (m)', 'Width (m)', 'Last Updated', 'Created At',
    ])

    vessels = Vessel.objects.all().order_by('name')
    for v in vessels:
        writer.writerow([
            v.mmsi, v.imo, v.name, v.callsign, v.vessel_type, v.flag, v.cargo,
            v.latitude, v.longitude, v.speed, v.course, v.heading,
            v.nav_status, v.destination, v.eta, v.draught,
            v.length, v.width, v.last_updated.isoformat(), v.created_at.isoformat(),
        ])

    logger.info(f'Admin CSV export: {vessels.count()} vessels exported by {request.user.email}')
    return response


# ─── CSV Export: Subscriptions ────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_subscriptions_csv(request):
    """
    GET /api/admin-api/export/subscriptions/
    Downloads all subscription data as a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="subscriptions_export_{timezone.now():%Y%m%d_%H%M%S}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'User Email', 'User Name', 'Vessel MMSI', 'Vessel Name',
        'Vessel Type', 'Notes', 'Subscribed At',
    ])

    subscriptions = Subscription.objects.select_related('user', 'vessel').all().order_by('-created_at')
    for s in subscriptions:
        writer.writerow([
            s.id, s.user.email, s.user.username,
            s.vessel.mmsi, s.vessel.name, s.vessel.vessel_type,
            s.notes, s.created_at.isoformat(),
        ])

    logger.info(f'Admin CSV export: {subscriptions.count()} subscriptions exported by {request.user.email}')
    return response
