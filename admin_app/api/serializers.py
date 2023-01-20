from admin_app.models import UserSearchHistory, Message
from rest_framework import serializers

class UserSearchHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSearchHistory
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'