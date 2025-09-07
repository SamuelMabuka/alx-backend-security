from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit


@csrf_exempt
@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
def login_authenticated(request):
    """
    Login endpoint for authenticated users (limited to 10 requests/minute).
    """
    if request.method == "POST":
        return JsonResponse({"message": "Authenticated login attempt"})
    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_anonymous(request):
    """
    Login endpoint for anonymous users (limited to 5 requests/minute).
    """
    if request.method == "POST":
        return JsonResponse({"message": "Anonymous login attempt"})
    return JsonResponse({"error": "Only POST allowed"}, status=405)
