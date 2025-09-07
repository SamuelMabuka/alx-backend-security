from django.http import HttpResponseForbidden
from django.core.cache import cache
from ipware import get_client_ip
from geoip2.database import Reader
from pathlib import Path
from .models import RequestLog, BlockedIP


class IPLoggingMiddleware:
    """
    Middleware to log IP address, timestamp, and request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR', '')
        
        # Block if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")
        
        # Geolocation lookup (with cache for 24h)
        geo_data = cache.get(f"geo:{ip}")
        if not geo_data:
            try:
                geo_data = geolocator.get(ip)  # returns dict
                cache.set(f"geo:{ip}", geo_data, timeout=60 * 60 * 24)  # 24 hours
            except Exception:
                geo_data = {}

        country = geo_data.get("country", "")
        city = geo_data.get("city", "")

        # Log request with geolocation
        try:
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                country=country,
                city=city,
            )
        except Exception as e:
            print(f"Failed to log request: {e}")

        # Log request
        try:
            RequestLog.objects.create(ip_address=ip, path=request.path)
        except Exception as e:
            print(f"Failed to log request: {e}")

        # Save log
        try:
            RequestLog.objects.create(ip_address=ip, path=request.path)
        except Exception as e:
            print(f"Failed to log request: {e}")

        # Continue processing request
        response = self.get_response(request)
        return response
