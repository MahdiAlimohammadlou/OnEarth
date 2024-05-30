from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import redis, string, random, requests, jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from .models import (User, Ticket, AgentInfo, BuyerPersonalInfo, SellerPersonalInfo)
from .serializers import (BuyerPersonalInfoSerializer, SellerPersonalInfoSerializer,
                           AgentInfoSerializer, TicketSerializer, UserSerializer,
                           ChangePasswordSerializer
                           )
from rest_framework.permissions import IsAuthenticated
from core.views import InfoAPIView
from account.models import User
from django.contrib.auth.tokens import default_token_generator

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


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password has been changed."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def generate_and_store_otp(request):
    '''
    This api view will take an email generate an otp code for the email in redis for 2 minutes.
    '''
    if request.method == 'POST':
        email = request.data.get('email')
        otp_code = ''.join(random.choices(string.digits, k=6))
        try:
            r = redis.Redis(host=settings.REDIS_HOST,
                            port=settings.REDIS_PORT,
                             db= settings.OTP_REDIS_DB,)
            r.setex(email, 180, otp_code)
            send_otp(email, otp_code)
            return Response({'detail': 'otp generated successfully'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'detail': 'otp generated failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    '''
    This api view will take (email, otp, phone number, password) and verify the otp.
    Finally, if verification is successful, the user will be signed up.
    '''
    if request.method == 'POST':
        try:
            email = request.data.get('email')
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')
            entered_otp = request.data.get('entered_otp')
            
            if not all([email, phone_number, password, entered_otp]):
                return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

            r = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.OTP_REDIS_DB,
            )
            
            stored_otp = r.get(email)
            
            if not stored_otp:
                return Response({"detail": "OTP not found or expired."}, status=status.HTTP_400_BAD_REQUEST)
            
            if stored_otp.decode('utf-8') != entered_otp:
                return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(email=email, password=password, phone_number=phone_number)
            tokens = get_tokens_for_user(user)
            
            return Response(
                {
                    "detail": "User signed up successfully",
                    "access": tokens["access"],
                    "refresh": tokens["refresh"]
                },
                status=status.HTTP_201_CREATED
            )
        except redis.RedisError as e:
            return Response({"detail": "Redis error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"detail": "An error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def check_user_existence(request, email):
    try:
        user = User.objects.get(email=email)
        return Response({'exists': True}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'exists': False}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_and_create_tokens(request):
    if request.method == "POST":
        token = request.data.get("token")
        if not token:
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return Response({'error': 'Token verification failed', 'details': response.json()}, status=status.HTTP_400_BAD_REQUEST)
            
            data = response.json()
            email = data.get('email')

            if not email:
                return Response({'error': 'Invalid token or email not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Find user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user if not found
                user = User.objects.create_user(email=email, username=email, password=None)

            user_tokens = get_tokens_for_user(user)
            return Response({'detail': 'OTP verification successful',
                            "refresh" : user_tokens["refresh"],
                            "access" : user_tokens["access"]
                            },
                            status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': 'Token verification failed', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.PyJWTError as e:
            return Response({'error': 'Token creation failed', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BuyerPersonalInfoAPIView(InfoAPIView):
    serializer_class = BuyerPersonalInfoSerializer
    model_class = BuyerPersonalInfo
    user_field = 'buyer_user'

class SellerPersonalInfoAPIView(InfoAPIView):
    serializer_class = SellerPersonalInfoSerializer
    model_class = SellerPersonalInfo
    user_field = 'seller_user'

class AgentInfoAPIView(InfoAPIView):
    serializer_class = AgentInfoSerializer
    model_class = AgentInfo
    user_field = 'agent_user'
    
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
