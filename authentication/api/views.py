from authentication.api.serializers import SignUpSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User


"""
view for user registration
"""
class SignUpVS(viewsets.ViewSet):

    def create(self, request):

        serializer = SignUpSerializer(data=request.data)

        data = {}

        # check if username and email are already regestered
        filter_username = User.objects.filter(username=serializer.initial_data['username'])
        filter_email = User.objects.filter(email=serializer.initial_data['email'])

        if filter_username.exists():
            raise ValidationError({'error': 'Username already exists!!'})
        
        if filter_email.exists():
            raise ValidationError({'error': 'Email already exists!!'})
        
        elif serializer.is_valid():
            
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']

            # check password and confirm password are same
            if password != confirm_password:
                raise ValidationError({'error': 'password & confirm password should be same!!'})

            # save user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            data['response'] = "Registration Successfull"
            data['username'] = user.username
            data['email'] = user.email

            # generate token
            refresh = RefreshToken.for_user(user)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_202_ACCEPTED)
        
        raise ValidationError({'message':'Please enter valid data'})