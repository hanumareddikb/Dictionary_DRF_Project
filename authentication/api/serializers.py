from rest_framework import serializers
from authentication.models import User

class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs ={
            'password': {'write_only': True}
        }