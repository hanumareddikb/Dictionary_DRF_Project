from dictionary.models import Dictionary

from rest_framework import serializers

class DictionarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Dictionary
        exclude = ('no_of_searches',)

class WordSerializer(serializers.Serializer):
    word = serializers.CharField(required=True)

class LetterSerializer(serializers.Serializer):
    letter = serializers.CharField(required=True, max_length=1)