# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render
from api.models import Prediction
from rest_framework import permissions
# third_party imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import MessageSerializer, PredictionSerializer
from .test import Message, Predict


@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def listmessage(request):
    query = request.GET.get('q','')
    request.session['text'] = query
    message_obj = Message(query,'hello')
    serializer_class = MessageSerializer(message_obj)
    return Response(serializer_class.data)

    
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def prediction(request):
    if request.method == 'GET':
        snippets = Prediction.objects.all()
        serializer = PredictionSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def textmessage(request):
    result = request.session['text']
    message_obj = Message(result,'content')
    serializer_class = MessageSerializer(message_obj)
    return Response(serializer_class.data)

    
