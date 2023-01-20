from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .serializers import ThoughtSerializer
from django.utils.timezone import now

import requests
import json

"""
view for thought of the day
"""
class Thought(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    def list(self, request):
        # get thoyght from api ninjas.com
        category = 'learning'
        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
        response = requests.get(api_url, headers={'X-Api-Key': 'XfllCBPmFtOTrmXNHg6EZQ==EBINPUjfGwcgI1cg'})
        if response.status_code == requests.codes.ok:
            str_data = json.dumps(response.json())
            json_data = json.loads(str_data)

            # retrieve qoute and author
            quote = json_data[0]['quote']
            author = json_data[0]['author']

            data = {'quote':quote,
                    'author':author,
                    }

            serializer = ThoughtSerializer(data)

            data = serializer.data
            data['date']=now().date()  # add date

            return Response(data, status=status.HTTP_302_FOUND)
            
        raise ValidationError({"message": "Internal server error"})