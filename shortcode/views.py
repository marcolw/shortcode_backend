from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from . import serializers
from . import models

import time
import requests


@api_view(['GET', 'POST'])
def test(request):
    print (request.user)
    print (request.user.is_authenticated)
    print (request.user.is_anonymous)
    print (len(requests.get('https://www.allendale-group.co.uk/shortcode/ShortcodeData.xml').text))
    
    return JsonResponse({
        "mystatus": 200
    })

class UploadFileView(APIView):
    # MultiPartParser AND FormParser
    # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
    # "You will typically want to use both FormParser and MultiPartParser
    # together in order to fully support HTML form data."
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = serializers.ProductFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            queryset = models.Product.objects.all()
            products = serializers.ProductSerializer(queryset, many=True)
            return Response(products.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
