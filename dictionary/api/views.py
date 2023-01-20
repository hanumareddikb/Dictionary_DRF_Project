from dictionary.models import Dictionary
from admin_app.models import UserSearchHistory
from .serializers import DictionarySerializer, WordSerializer, LetterSerializer
from .pagination import WordsPaginater

from django.core.mail import send_mail
from django.utils.timezone import now

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

import requests
import random
import json


"""
view to search word
"""
class SearchWordVS(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    def create(self, request):
        serializer = WordSerializer(data=request.data)

        if serializer.is_valid():
            word = serializer.validated_data['word']

            # save user search history
            user_search_history = UserSearchHistory()
            user_search_history.username = request.user.username
            user_search_history.word = word
            user_search_history.time = now()
            user_search_history.save()

            # check if the required word already exists in db(ie. in Dictionary model)
            # if exists, than display the same with it's meaning to user
            try:
                queryset = Dictionary.objects.get(word=word)
                queryset.no_of_searches += 1
                queryset.save()
                serializer = DictionarySerializer(queryset)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # if user searches the word for first time(ie. required word doesn't exists)
            # than call the api oxforddictionaries.com
            except Dictionary.DoesNotExist:
                app_id = 'c620484d'
                app_key = 'ec69a65ad0fc39db0f8034af556396c4'
                language = 'en-gb'
                url = 'https://od-api.oxforddictionaries.com/api/v2/entries/'  + language + '/'  + word.lower()
                response = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})

                if response.status_code == requests.codes.ok:
                    str_data = json.dumps(response.json())
                    dict_data = json.loads(str_data)

                    try:
                        meaning = dict_data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
                        examples = dict_data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples']
                        l = []
                        for i in examples:
                            for key in i.keys():
                                l.append(i[key])

                        try:
                            example_1 = l[0]
                        except IndexError:
                            example_1 = "None"

                        try:
                            example_2 = l[1]
                        except IndexError:
                            example_2 = "None"
                        
                        # save the word and it's meaning in db(ie. in Dictionary model)
                        dict = Dictionary()
                        dict.word = word.lower()
                        dict.meaning = meaning
                        dict.example_1 = example_1
                        dict.example_2 = example_2
                        dict.save()

                        # get user email
                        email = request.user.email

                        # send email to user
                        send_mail("Your word meaning from MyDictionary",
                                    f"Word: {word}\nMeaning: {meaning}\nExample 1: {example_1}\nExample 1: {example_2}",
                                    "mailtrap@mydictionary.com",
                                    [f'{email}'])

                        # display the results to user
                        queryset = Dictionary.objects.get(word=word)
                        queryset.no_of_searches += 1
                        queryset.save()
                        serializer = DictionarySerializer(queryset)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    
                    except KeyError:
                        raise ValidationError({'message':'Sorry!! Your word not found'})

                raise ValidationError({"message": "Internal server error"})
        
        raise ValidationError({"message": "Enter valid word"})


"""
view to list all words
"""
class ListWordsVS(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]
    pagination_class = WordsPaginater

    def list(self, request):
        queryset = Dictionary.objects.order_by('word')
        paginator = WordsPaginater()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = DictionarySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = DictionarySerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_302_FOUND)


"""
view for word of the day
"""
class WordOfTheDay(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    def list(self, request):
        all_objects = Dictionary.objects.all()

        # get random word
        queryset = random.choice(all_objects)
        serializer = DictionarySerializer(queryset)
        data = serializer.data
        data['date']=now().date()
        return Response(data, status=status.HTTP_302_FOUND)


"""
view for latest word added
"""
class LatestWord(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    def list(self, request):
        queryset = Dictionary.objects.last() # last object in the table
        serializer = DictionarySerializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


"""
view for most sarched word
"""
class MostSearchedWord(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    def list(self, request):
        queryset = Dictionary.objects.order_by('no_of_searches').last()
        serializer = DictionarySerializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


"""
view to list all words with filter
"""
class ListWordsWithLetter(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    def create(self, request):
        serializer = LetterSerializer(data=request.data)
        if serializer.is_valid():
            letter = serializer.validated_data['letter']
            queryset = Dictionary.objects.filter(word__istartswith = letter)

            # check if word with request letter exists or not
            if queryset :
                serializer = DictionarySerializer(queryset, many = True)
                return Response(serializer.data, status=status.HTTP_302_FOUND)

            raise ValidationError({'message':'Words with this letter does not exist'})

        raise ValidationError({'message':'Enter a valid letter'})