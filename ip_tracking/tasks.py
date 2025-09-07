from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_suspicious_ips():
    """
    Run hourly:
    - Flag IPs exceeding 100 requests in the past hour.
    - Flag IPs accessing sensitive paths (/admin, /login).
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Count requests per IP
    ip_counts = {}
    for log in logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

        # Rule 1: Sensitive path access
        if log.path.startswith("/admin") or log.path.startswith("/login"):
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                defaults={"reason": f"Accessed sensitive path {log.path}"},
            )

    # Rule 2: Exceeded 100 requests/hour
    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={"reason": f"Exceeded {count} requests in the past hour"},
            )
