from rest_framework import serializers

class ThoughtSerializer(serializers.Serializer):
    quote = serializers.CharField()
    author = serializers.CharField()