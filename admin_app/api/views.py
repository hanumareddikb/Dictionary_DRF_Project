from admin_app.api.serializers import UserSearchHistorySerializer, MessageSerializer
from admin_app.models import UserSearchHistory, Message
from admin_app.api.permissions import AdminUserOrWriteOnly

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ValidationError

"""
view for user search history
"""
class UserSearchHistoryVS(viewsets.ViewSet):

    permission_classes = [IsAdminUser]

    def list(self, request):
        queryset = UserSearchHistory.objects.all()
        serializer = UserSearchHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    def retrieve(self, request, pk):
        queryset = UserSearchHistory.objects.all()
        message = get_object_or_404(queryset, pk=pk)
        serializer = UserSearchHistorySerializer(message)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    def delete(self, request, pk):
        message = UserSearchHistory.objects.get(pk=pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
view for user messages
"""
class MessageVS(viewsets.ViewSet):

    permission_classes = [AdminUserOrWriteOnly]

    def list(self, request):
        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

    def create(self, request):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # send user message to admin by email
            send_mail("MyDictionary user message",
                f"Name: {serializer.validated_data['name']}\nEmail: {serializer.validated_data['email']}\nSubject: {serializer.data['subject']}\nMessage: {serializer.data['message']}",
                f"{serializer.validated_data['email']}",
                ["reddibentur@gmail.com"])
                
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        raise ValidationError({'message':'Please enter valid data'})

    def retrieve(self, request, pk):
        queryset = Message.objects.all()
        message = get_object_or_404(queryset, pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

    def delete(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)