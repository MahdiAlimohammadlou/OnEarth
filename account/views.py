from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import redis, requests, jwt
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
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from account.utils import (validate_email_and_user, verify_otp, get_tokens_for_user,
                            get_device_info, generate_and_send_otp, validate_email_and_password,
                            store_otp_in_redis)

def create_device_and_response(user, device_info, tokens):
    device, created = Device.objects.get_or_create(
        user=user, 
        device_info=device_info,
        defaults={'refresh_token': tokens['refresh']}
    )
    
    if not created and device.is_token_expired():
        device.refresh_token = tokens['refresh']
        device.save()
        
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
def generate_otp_sign_in(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if email and password are provided
        if not email or not password:
            return Response({'detail': 'Email and password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email and password
        error, status_code = validate_email_and_password(email, password)
        if error:
            return Response(error, status=status_code)

        # Generate and send OTP
        response, status_code = generate_and_send_otp(email)
        return Response(response, status=status_code)
    
@api_view(['POST'])
def generate_otp_sign_up(request):
    if request.method == 'POST':
        email = request.data.get('email')

        # Check if email is provided
        if not email:
            return Response({'detail': 'Email field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email and check if user does not exist
        error, status_code = validate_email_and_user(email, should_exist=False)
        if error:
            return Response(error, status=status_code)

        # Generate and send OTP
        response, status_code = generate_and_send_otp(email)
        return Response(response, status=status_code)
    
@api_view(['POST'])
def generate_otp_forgot(request):
    if request.method == 'POST':
        email = request.data.get('email')

        # Check if email is provided
        if not email:
            return Response({'detail': 'Email field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email and check if user does not exist
        error, status_code = validate_email_and_user(email, should_exist=True)
        if error:
            return Response(error, status=status_code)

        # Generate and send OTP
        response, status_code = generate_and_send_otp(email)
        return Response(response, status=status_code)

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
            return Response({"detail": "Please fill in all fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_verification = verify_otp(email, entered_otp)
        if not otp_verification["status"]:
            return Response({"detail": "Your OTP code is wrong."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Check user existence
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({"detail": "The password is incorrect."}, status=status.HTTP_401_UNAUTHORIZED)
            # Generate token for user
            tokens = get_tokens_for_user(user)
            device_info = get_device_info(request)
            return create_device_and_response(user, device_info, tokens)
        except User.DoesNotExist:
            return Response({"detail": "No user found with this email."}, status=status.HTTP_404_NOT_FOUND)
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
            return Response({"detail": "Please fill in all fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_verification = verify_otp(email, entered_otp)
        if not otp_verification["status"]:
            return Response({"detail": "The OTP is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
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
def verify_otp_forgot(request):
    if request.method == 'POST':
        email = request.data.get('email')
        entered_otp = request.data.get('otp')

        # Check if email and otp are provided
        if not email or not entered_otp:
            return Response({'detail': 'Email and OTP fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify OTP
        verification_result = verify_otp(email, entered_otp)
        if verification_result['status']:
            store_otp_in_redis(email, entered_otp, 900)
            return Response({'detail': 'OTP is correct.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': verification_result['detail']}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def reset_password_with_otp(request):
    if request.method == 'POST':
        email = request.data.get('email')
        entered_otp = request.data.get('otp')
        new_password = request.data.get('password')
        re_password = request.data.get('repassword')

        # Check if all fields are provided
        if not email or not entered_otp or not new_password or not re_password:
            return Response({'detail': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if passwords match
        if new_password != re_password:
            return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify OTP
        verification_result = verify_otp(email, entered_otp)
        if not verification_result['status']:
            return Response({'detail': verification_result['detail']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Set new password
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

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
