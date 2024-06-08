from rest_framework.response import Response
import redis
from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from user_agents import parse

def verify_otp(email, entered_otp):
    # Connect to Redis
    r = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.OTP_REDIS_DB,
    )
    # Retrieve OTP from Redis
    stored_otp = r.get(email)
    if not stored_otp:
        return {"status": False, "detail": "OTP not found or expired."}
    if stored_otp.decode('utf-8') != entered_otp:
        return {"status": False, "detail": "Invalid OTP."}
    return {"status": True}

def send_otp(to, otp):
    subject = "OnEarth Code"
    text = "Your entrance code : " + otp
    send_mail(subject, text, settings.EMAIL_HOST_USER, [to])

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_device_name(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    if device := user_agent.device.family:
        return device
    return "Unknown Device"

def get_device_info(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    
    device_info = f"{user_agent.os.family} {user_agent.os.version_string} {user_agent.browser.family} {user_agent.browser.version_string} {user_agent.device.family}"
        
    return device_info
