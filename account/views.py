from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import redis, string, random, requests, jwt
from django.conf import settings
from .models import (User, Ticket, AgentInfo, BuyerPersonalInfo, SellerPersonalInfo, Device)
from .serializers import (BuyerPersonalInfoSerializer, SellerPersonalInfoSerializer,
                           AgentInfoSerializer, TicketSerializer, UserSerializer,
                           ChangePasswordSerializer, CreateOrUpdateAgentInfoSerializer,
                           CreateOrUpdateSellerPersonalInfoSerializer,
                           CreateOrUpdateBuyerPersonalInfoSerializer,
                           DeviceSerializer,
                           )
from rest_framework.permissions import IsAuthenticated
from core.views import InfoAPIView
from account.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from account.utils import verify_otp, get_tokens_for_user, send_otp, get_device_info

def create_device_and_response(user, device_info, tokens):
    if not Device.objects.filter(user=user, device_info=device_info).exists():
        Device.objects.create(
            user=user,
            device_info=device_info,
            refresh_token = tokens['refresh']
        )
    return Response({
        'access': tokens['access'],
        'refresh': tokens['refresh']
    })


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
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # Validate new password
            try:
                validate_password(serializer.validated_data['new_password'], user=user)
            except ValidationError as e:
                return Response({"new_password": e.messages}, status=status.HTTP_400_BAD_REQUEST)
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password has been changed."}, status=status.HTTP_200_OK)
        # Return serializer errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def generate_and_store_otp(request):
    '''
    This API view takes an email, generates an OTP code for the email,
    and stores it in Redis for 2 minutes.
    '''
    if request.method == 'POST':
        email = request.data.get('email')

        # Check if email is provided
        if not email:
            return Response({'detail': 'Email field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = ''.join(random.choices(string.digits, k=6))
        
        try:
            r = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.OTP_REDIS_DB,
            )
            r.setex(email, 180, otp_code)
            send_otp(email, otp_code)
            return Response({'detail': 'OTP generated successfully.'}, status=status.HTTP_201_CREATED)
        
        except redis.exceptions.ConnectionError:
            return Response({'detail': 'Failed to connect to Redis.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def sign_in_verify_otp(request):
    '''
    This api view will take (email, otp, password) and verify the otp.
    Finally, if verification is successful, the user will be signed in.
    '''
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        entered_otp = request.data.get('entered_otp')
        # Check if all required fields are provided
        if not all([email, password, entered_otp]):
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_verification = verify_otp(email, entered_otp)
        if not otp_verification["status"]:
            return Response({"detail": otp_verification["detail"]}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Check user existence
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({"error": "Invalid Password"}, status=status.HTTP_401_UNAUTHORIZED)
            # Generate token for user
            tokens = get_tokens_for_user(user)
            device_info = get_device_info(request)
            return create_device_and_response(user, device_info, tokens)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except redis.RedisError as e:
        return Response({"detail": "Redis error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"detail": "An error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def sign_up_verify_otp(request):
    '''
    This api view will take (email, otp, phone number, password) and verify the otp.
    Finally, if verification is successful, the user will be signed up.
    '''
    try:
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        entered_otp = request.data.get('entered_otp')
        # Check if all required fields are provided
        if not all([email, phone_number, password, entered_otp]):
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_verification = verify_otp(email, entered_otp)
        if not otp_verification["status"]:
            return Response({"detail": otp_verification["detail"]}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for unique email and phone number
        if User.objects.filter(email=email).exists():
            return Response({"detail": "This email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"detail": "This phone number is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = User.objects.create_user(email=email, password=password, phone_number=phone_number)
        tokens = get_tokens_for_user(user)
        device_info = get_device_info(request)
        return create_device_and_response(user, device_info, tokens)
    except redis.RedisError as e:
        return Response({"detail": "Redis error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"detail": "An error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def refresh_jwt(request):
    try:
        refresh_token = request.data.get('refresh_token')
        refresh = RefreshToken(refresh_token)
        new_access_token = refresh.access_token
        return Response({
            'access': str(new_access_token),
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_jwt(request):
    try:
        serializer = TokenVerifySerializer(data={'token': request.data.get('token')})
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_user_existence(request, email):
    if not email:
        return Response({'error': 'Email cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        return Response({'exists': True}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'exists': False}, status=status.HTTP_200_OK)
    except User.MultipleObjectsReturned:
        return Response({'error': 'The entered email is not unique.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_and_create_tokens(request):
    if request.method == "POST":
        token = request.data.get("token")
        if not token:
            return Response({'error': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return Response({'error': 'Token verification failed.', 'details': response.json()}, status=status.HTTP_400_BAD_REQUEST)
            
            data = response.json()
            email = data.get('email')

            if not email:
                return Response({'error': 'Invalid token or email not found.'}, status=status.HTTP_400_BAD_REQUEST)

            # Find user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user if not found
                user = User.objects.create_user(email=email, username=email, password=None)
            except User.MultipleObjectsReturned:
                return Response({'error': 'The entered email is not unique.'}, status=status.HTTP_400_BAD_REQUEST)

            user_tokens = get_tokens_for_user(user)
            return Response({'detail': 'OTP verification successful',
                            "refresh": user_tokens["refresh"],
                            "access": user_tokens["access"]
                            },
                            status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': 'Token verification failed.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.PyJWTError as e:
            return Response({'error': 'Token creation failed.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BuyerPersonalInfoAPIView(InfoAPIView):
    serializer_class = BuyerPersonalInfoSerializer
    model_class = BuyerPersonalInfo
    create_or_update_serializer_class = CreateOrUpdateBuyerPersonalInfoSerializer
    user_field = 'buyer_user'

class SellerPersonalInfoAPIView(InfoAPIView):
    serializer_class = SellerPersonalInfoSerializer
    model_class = SellerPersonalInfo
    create_or_update_serializer_class = CreateOrUpdateSellerPersonalInfoSerializer
    user_field = 'seller_user'

class AgentInfoAPIView(InfoAPIView):
    serializer_class = AgentInfoSerializer
    model_class = AgentInfo
    create_or_update_serializer_class = CreateOrUpdateAgentInfoSerializer
    user_field = 'agent_user'
    
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)

class RevokeTokenView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()

    def delete(self, request, *args, **kwargs):
        device = self.get_object()
        if device.user != request.user:
            return Response({"detail" : "The selected device does not belong to this account."} , status=status.HTTP_403_FORBIDDEN)
        
        device.blacklist_tokens()
        device.delete()
        return Response({"detail" : "device removed successfully."}, status=status.HTTP_204_NO_CONTENT)
