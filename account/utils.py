import redis
from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from user_agents import parse
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from account.models import User
import random, string
from django.contrib.auth import authenticate

def validate_email_and_password(email, password):
    # Validate the email format
    try:
        validate_email(email)
    except ValidationError:
        return {'detail': 'Please provide a valid email address.'}, status.HTTP_400_BAD_REQUEST

    # Check if user exists and authenticate
    user = authenticate(email=email, password=password)
    if user is None:
        return {'detail': 'Invalid email or password.'}, status.HTTP_401_UNAUTHORIZED

    return None, None

def generate_and_send_otp(email):
    otp_code = ''.join(random.choices(string.digits, k=6))
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.OTP_REDIS_DB,
        )
        r.setex(email, 180, otp_code)
        send_otp(email, otp_code)
        return {'detail': 'OTP generated and sent successfully.'}, status.HTTP_201_CREATED
    except redis.exceptions.ConnectionError:
        return {'detail': 'Failed to connect to Redis.'}, status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return {'detail': f'An error occurred: {str(e)}'}, status.HTTP_500_INTERNAL_SERVER_ERROR


def validate_email_and_user(email, should_exist=True):
    # Validate the email format
    try:
        validate_email(email)
    except ValidationError:
        return {'detail': 'Please provide a valid email address.'}, status.HTTP_400_BAD_REQUEST
    
    # Check if user exists or not
    user_exists = User.objects.filter(email=email).exists()
    if should_exist and not user_exists:
        return {'detail': 'User with this email does not exist.'}, status.HTTP_404_NOT_FOUND
    if not should_exist and user_exists:
        return {'detail': 'User with this email already exists.'}, status.HTTP_400_BAD_REQUEST

    return None, None

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
        return {"status": False, "detail": "Your OTP not found or expired."}
    if stored_otp.decode('utf-8') != entered_otp:
        return {"status": False, "detail": "Your OTP code is wrong."}
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
