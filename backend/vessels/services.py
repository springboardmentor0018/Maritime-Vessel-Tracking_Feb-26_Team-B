"""
Vessels services — AIS Hub API client with demo/mock data fallback
"""
import logging
import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

# ─── Demo Data ───────────────────────────────────────────────────────────────
# Realistic mock vessel data used when no AIS_API_KEY is configured.
DEMO_VESSELS = [
    {
        'mmsi': '211331640',
        'imo': '9183163',
        'name': 'EVER GIVEN',
        'callsign': 'H3RC',
        'vessel_type': 'Cargo',
        'flag': 'Panama',
        'cargo': 'Container',
        'latitude': 31.3856,
        'longitude': 32.3617,
        'speed': 12.4,
        'course': 185.0,
        'heading': 183,
        'nav_status': 'Under way using engine',
        'destination': 'ROTTERDAM',
        'eta': '2026-02-25 14:00',
        'draught': 16.0,
        'length': 400.0,
        'width': 59.0,
    },
    {
        'mmsi': '353136000',
        'imo': '9461867',
        'name': 'MAERSK EDINBURGH',
        'callsign': 'C6FS9',
        'vessel_type': 'Cargo',
        'flag': 'Denmark',
        'cargo': 'Container',
        'latitude': 51.9244,
        'longitude': 4.4777,
        'speed': 0.0,
        'course': 0.0,
        'heading': 90,
        'nav_status': 'Moored',
        'destination': 'SINGAPORE',
        'eta': '2026-03-10 08:00',
        'draught': 14.5,
        'length': 366.0,
        'width': 48.2,
    },
    {
        'mmsi': '636092772',
        'imo': '9839430',
        'name': 'CMA CGM JACQUES SAADE',
        'callsign': 'A8FJ7',
        'vessel_type': 'Cargo',
        'flag': 'France',
        'cargo': 'Container',
        'latitude': 36.1408,
        'longitude': -5.3536,
        'speed': 18.2,
        'course': 270.0,
        'heading': 268,
        'nav_status': 'Under way using engine',
        'destination': 'LE HAVRE',
        'eta': '2026-02-22 06:00',
        'draught': 15.5,
        'length': 400.0,
        'width': 61.0,
    },
    {
        'mmsi': '563000780',
        'imo': '9334857',
        'name': 'PACIFIC VOYAGER',
        'callsign': '9V8836',
        'vessel_type': 'Tanker',
        'flag': 'Singapore',
        'cargo': 'Crude Oil',
        'latitude': 1.2644,
        'longitude': 103.8196,
        'speed': 0.1,
        'course': 45.0,
        'heading': 180,
        'nav_status': 'At anchor',
        'destination': 'JEDDAH',
        'eta': '2026-03-01 12:00',
        'draught': 21.0,
        'length': 333.0,
        'width': 60.0,
    },
    {
        'mmsi': '311000593',
        'imo': '9697753',
        'name': 'HARMONY OF THE SEAS',
        'callsign': 'C6GQ9',
        'vessel_type': 'Passenger',
        'flag': 'Bahamas',
        'cargo': 'Passengers',
        'latitude': 25.7617,
        'longitude': -80.1918,
        'speed': 0.0,
        'course': 0.0,
        'heading': 270,
        'nav_status': 'Moored',
        'destination': 'COZUMEL',
        'eta': '2026-02-21 07:00',
        'draught': 9.3,
        'length': 362.0,
        'width': 66.0,
    },
    {
        'mmsi': '367596000',
        'imo': '8863916',
        'name': 'ATLANTIC PIONEER',
        'callsign': 'WDD8774',
        'vessel_type': 'Fishing',
        'flag': 'United States',
        'cargo': 'Fish',
        'latitude': 41.3256,
        'longitude': -69.1208,
        'speed': 6.2,
        'course': 110.0,
        'heading': 108,
        'nav_status': 'Engaged in fishing',
        'destination': 'NEW BEDFORD',
        'eta': '2026-02-20 18:00',
        'draught': 4.5,
        'length': 45.0,
        'width': 12.0,
    },
    {
        'mmsi': '244780961',
        'imo': '9480626',
        'name': 'DUTCH SPIRIT',
        'callsign': 'PBDM',
        'vessel_type': 'Tug',
        'flag': 'Netherlands',
        'cargo': 'None',
        'latitude': 51.9075,
        'longitude': 4.5019,
        'speed': 3.4,
        'course': 80.0,
        'heading': 78,
        'nav_status': 'Under way using engine',
        'destination': 'EUROPOORT',
        'eta': '2026-02-20 16:00',
        'draught': 6.2,
        'length': 70.0,
        'width': 16.0,
    },
    {
        'mmsi': '235082034',
        'imo': '9150082',
        'name': 'HMS QUEEN ELIZABETH',
        'callsign': 'GCVN',
        'vessel_type': 'Military',
        'flag': 'United Kingdom',
        'cargo': 'Military',
        'latitude': 50.8054,
        'longitude': -1.1084,
        'speed': 0.0,
        'course': 0.0,
        'heading': 0,
        'nav_status': 'Moored',
        'destination': 'PORTSMOUTH',
        'eta': '',
        'draught': 11.0,
        'length': 284.0,
        'width': 73.0,
    },
    {
        'mmsi': '538006452',
        'imo': '9706891',
        'name': 'OCEAN GRACE',
        'callsign': 'V7GR8',
        'vessel_type': 'Tanker',
        'flag': 'Marshall Islands',
        'cargo': 'LNG',
        'latitude': 26.2285,
        'longitude': 50.5860,
        'speed': 14.8,
        'course': 135.0,
        'heading': 133,
        'nav_status': 'Under way using engine',
        'destination': 'TOKYO BAY',
        'eta': '2026-03-05 20:00',
        'draught': 12.1,
        'length': 295.0,
        'width': 46.0,
    },
    {
        'mmsi': '413876004',
        'imo': '9455291',
        'name': 'COSCO SHIPPING UNIVERSE',
        'callsign': 'VRHE3',
        'vessel_type': 'Cargo',
        'flag': 'China',
        'cargo': 'Container',
        'latitude': 22.2872,
        'longitude': 114.1580,
        'speed': 0.2,
        'course': 340.0,
        'heading': 220,
        'nav_status': 'Moored',
        'destination': 'LONG BEACH',
        'eta': '2026-03-15 08:00',
        'draught': 15.8,
        'length': 400.0,
        'width': 58.6,
    },
    {
        'mmsi': '256728000',
        'imo': '9198928',
        'name': 'MALTA STAR',
        'callsign': '9HBC7',
        'vessel_type': 'Cargo',
        'flag': 'Malta',
        'cargo': 'Bulk Grain',
        'latitude': 35.8989,
        'longitude': 14.5146,
        'speed': 11.1,
        'course': 90.0,
        'heading': 88,
        'nav_status': 'Under way using engine',
        'destination': 'ALEXANDRIA',
        'eta': '2026-02-23 04:00',
        'draught': 10.5,
        'length': 190.0,
        'width': 32.0,
    },
    {
        'mmsi': '477118800',
        'imo': '9820200',
        'name': 'ORIENTAL DRAGON',
        'callsign': 'VRGN7',
        'vessel_type': 'Tanker',
        'flag': 'Hong Kong',
        'cargo': 'Petroleum Products',
        'latitude': 12.5891,
        'longitude': 47.6512,
        'speed': 13.5,
        'course': 255.0,
        'heading': 252,
        'nav_status': 'Under way using engine',
        'destination': 'RAS TANURA',
        'eta': '2026-02-24 10:00',
        'draught': 18.0,
        'length': 336.0,
        'width': 60.0,
    },
    {
        'mmsi': '220543000',
        'imo': '9321483',
        'name': 'NORDIC BREEZE',
        'callsign': 'OYLW',
        'vessel_type': 'Cargo',
        'flag': 'Denmark',
        'cargo': 'Vehicles',
        'latitude': 57.7089,
        'longitude': 11.9746,
        'speed': 15.3,
        'course': 200.0,
        'heading': 198,
        'nav_status': 'Under way using engine',
        'destination': 'BREMERHAVEN',
        'eta': '2026-02-21 22:00',
        'draught': 8.9,
        'length': 200.0,
        'width': 32.2,
    },
    {
        'mmsi': '228186800',
        'imo': '9454399',
        'name': 'TAHITI NUI',
        'callsign': 'FNPA',
        'vessel_type': 'Passenger',
        'flag': 'France',
        'cargo': 'Passengers',
        'latitude': -17.5354,
        'longitude': -149.5666,
        'speed': 18.0,
        'course': 310.0,
        'heading': 308,
        'nav_status': 'Under way using engine',
        'destination': 'BORA BORA',
        'eta': '2026-02-21 12:00',
        'draught': 7.5,
        'length': 168.0,
        'width': 24.0,
    },
    {
        'mmsi': '710004890',
        'imo': '9287888',
        'name': 'SAO PAULO SPIRIT',
        'callsign': 'PPFD',
        'vessel_type': 'Tanker',
        'flag': 'Brazil',
        'cargo': 'Crude Oil',
        'latitude': -23.9551,
        'longitude': -46.3294,
        'speed': 0.0,
        'course': 0.0,
        'heading': 90,
        'nav_status': 'Moored',
        'destination': 'HOUSTON',
        'eta': '2026-03-08 14:00',
        'draught': 20.5,
        'length': 274.0,
        'width': 48.0,
    },
    {
        'mmsi': '566749000',
        'imo': '9702478',
        'name': 'SINGAPORE EXPRESS',
        'callsign': '9VIP3',
        'vessel_type': 'Cargo',
        'flag': 'Singapore',
        'cargo': 'Container',
        'latitude': 1.1504,
        'longitude': 103.7500,
        'speed': 8.5,
        'course': 350.0,
        'heading': 348,
        'nav_status': 'Under way using engine',
        'destination': 'COLOMBO',
        'eta': '2026-02-26 16:00',
        'draught': 13.2,
        'length': 300.0,
        'width': 48.2,
    },
    {
        'mmsi': '246273000',
        'imo': '9436015',
        'name': 'WINDWARD HUNTER',
        'callsign': 'PHRU',
        'vessel_type': 'Fishing',
        'flag': 'Netherlands',
        'cargo': 'Fish',
        'latitude': 54.0123,
        'longitude': 2.7891,
        'speed': 4.1,
        'course': 60.0,
        'heading': 58,
        'nav_status': 'Engaged in fishing',
        'destination': 'IJMUIDEN',
        'eta': '2026-02-22 10:00',
        'draught': 5.0,
        'length': 55.0,
        'width': 13.0,
    },
    {
        'mmsi': '261721000',
        'imo': '9511190',
        'name': 'BALTIC TRADER',
        'callsign': 'SPMQ',
        'vessel_type': 'Cargo',
        'flag': 'Poland',
        'cargo': 'General Cargo',
        'latitude': 54.3520,
        'longitude': 18.6466,
        'speed': 10.0,
        'course': 45.0,
        'heading': 43,
        'nav_status': 'Under way using engine',
        'destination': 'ST PETERSBURG',
        'eta': '2026-02-23 20:00',
        'draught': 7.8,
        'length': 140.0,
        'width': 21.0,
    },
    {
        'mmsi': '431000182',
        'imo': '9390912',
        'name': 'SAKURA MARU',
        'callsign': 'JD3812',
        'vessel_type': 'Cargo',
        'flag': 'Japan',
        'cargo': 'Vehicles',
        'latitude': 34.6937,
        'longitude': 135.5023,
        'speed': 0.0,
        'course': 0.0,
        'heading': 180,
        'nav_status': 'Moored',
        'destination': 'LOS ANGELES',
        'eta': '2026-03-12 06:00',
        'draught': 9.5,
        'length': 199.0,
        'width': 32.3,
    },
    {
        'mmsi': '503169200',
        'imo': '9765432',
        'name': 'SOUTHERN CROSS',
        'callsign': 'VKH891',
        'vessel_type': 'Sailing',
        'flag': 'Australia',
        'cargo': 'None',
        'latitude': -33.8688,
        'longitude': 151.2093,
        'speed': 7.2,
        'course': 120.0,
        'heading': 118,
        'nav_status': 'Under sail',
        'destination': 'AUCKLAND',
        'eta': '2026-03-01 08:00',
        'draught': 3.2,
        'length': 25.0,
        'width': 8.0,
    },
]


class AISHubService:
    """
    Service for fetching vessel data from AIS Hub API.
    Falls back to demo data when no API key is configured.
    """

    BASE_URL = 'http://data.aishub.net/ws.php'

    def __init__(self):
        self.api_key = getattr(settings, 'AIS_API_KEY', '')
        self.is_demo_mode = not bool(self.api_key)

    def fetch_vessels(self):
        """
        Fetch all vessels from AIS Hub API (or demo data).
        Updates the local Vessel cache and returns the queryset.
        """
        from .models import Vessel

        if self.is_demo_mode:
            logger.info('AIS Hub: Using demo data (no API key configured)')
            return self._load_demo_data()

        try:
            params = {
                'username': self.api_key,
                'format': '1',  # JSON
                'output': 'json',
                'compress': '0',
            }
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # AIS Hub returns a list with metadata at index 0 and vessel data at index 1
            if isinstance(data, list) and len(data) > 1:
                vessels_data = data[1]
                self._update_vessel_cache(vessels_data)
            else:
                logger.warning('AIS Hub: Unexpected response format')

        except requests.RequestException as e:
            logger.error(f'AIS Hub API error: {e}')
        except (ValueError, KeyError) as e:
            logger.error(f'AIS Hub data parsing error: {e}')

        return Vessel.objects.all()

    def get_vessel_by_mmsi(self, mmsi):
        """Get a single vessel by MMSI, fetching from API if not cached."""
        from .models import Vessel

        try:
            vessel = Vessel.objects.get(mmsi=mmsi)
            return vessel
        except Vessel.DoesNotExist:
            # Try to fetch from API
            if not self.is_demo_mode:
                self.fetch_vessels()
                try:
                    return Vessel.objects.get(mmsi=mmsi)
                except Vessel.DoesNotExist:
                    pass
            return None

    def _load_demo_data(self):
        """Load demo vessel data into the database."""
        from .models import Vessel

        for vessel_data in DEMO_VESSELS:
            Vessel.objects.update_or_create(
                mmsi=vessel_data['mmsi'],
                defaults=vessel_data
            )

        return Vessel.objects.all()

    def _update_vessel_cache(self, vessels_data):
        """Update local vessel cache from AIS Hub API response."""
        from .models import Vessel

        for v in vessels_data:
            try:
                Vessel.objects.update_or_create(
                    mmsi=str(v.get('MMSI', '')),
                    defaults={
                        'imo': str(v.get('IMO', '')),
                        'name': v.get('NAME', 'Unknown'),
                        'callsign': v.get('CALLSIGN', ''),
                        'vessel_type': self._map_vessel_type(v.get('TYPE', 0)),
                        'flag': v.get('FLAG', ''),
                        'latitude': v.get('LATITUDE'),
                        'longitude': v.get('LONGITUDE'),
                        'speed': v.get('SOG'),
                        'course': v.get('COG'),
                        'heading': v.get('HEADING'),
                        'nav_status': v.get('NAVSTAT', ''),
                        'destination': v.get('DESTINATION', ''),
                        'eta': v.get('ETA', ''),
                        'draught': v.get('DRAUGHT'),
                        'length': v.get('A', 0) + v.get('B', 0) if v.get('A') else None,
                        'width': v.get('C', 0) + v.get('D', 0) if v.get('C') else None,
                    }
                )
            except Exception as e:
                logger.error(f'Error caching vessel {v.get("MMSI")}: {e}')

    @staticmethod
    def _map_vessel_type(type_code):
        """Map AIS vessel type code to human-readable type."""
        type_map = {
            range(70, 80): 'Cargo',
            range(80, 90): 'Tanker',
            range(60, 70): 'Passenger',
            range(30, 38): 'Fishing',
            range(31, 33): 'Tug',
            range(50, 56): 'Pilot',
            range(35, 37): 'Military',
            range(36, 38): 'Sailing',
            range(37, 38): 'Pleasure',
            range(40, 50): 'HSC',
            range(51, 52): 'SAR',
        }
        for code_range, vessel_type in type_map.items():
            if type_code in code_range:
                return vessel_type
        return 'Other'
