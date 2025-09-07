from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)  # IPv4 + IPv6
    path = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.ip_address} -> {self.path} @ {self.timestamp}"

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return f"Blocked: {self.ip_address}"

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"