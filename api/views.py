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
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
from typing import List
import time

import os
import pprint

tokenizer = AutoTokenizer.from_pretrained(
    "/home/suyog/nepali-language-model/NepaliMaskedLM", use_auth_token=True
)

model = AutoModelForMaskedLM.from_pretrained(
    "/home/suyog/nepali-language-model/NepaliMaskedLM", use_auth_token=True
)

unmasker = pipeline("fill-mask", model=model, tokenizer=tokenizer)


@api_view(["GET", "POST"])
# @permission_classes([permissions.IsAuthenticated])
def listmessage(request):
    query = request.GET.get("q", "")
    request.session["text"] = query
    message_obj = Message(query, "content")
    serializer_class = MessageSerializer(message_obj)
    return Response(serializer_class.data)


@api_view(["GET", "POST"])
def prediction(request):
    if request.method == "GET":
        input_text: str = request.session.get("text", "")
        if not input_text:
            raise ValueError("No input text")
        masked_text: str = f"{input_text.rstrip()} <mask>"
        predictions = unmasker([masked_text], top_k=20)
        Prediction.objects.all().delete()
        filters = ["!!!", "...", ".", "..", "!!", "!", "....", "....."]

        predictions_filtered = list(
            filter(lambda x: x["token_str"] not in filters, predictions)
        )
        obj_list = [
            Prediction(prediction=pred["token_str"])
            for pred in predictions_filtered[:5]
        ]
        pprint.pprint(predictions_filtered[:5])

        snippets = obj_list[::-1]
        serializer = PredictionSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# @permission_classes([permissions.IsAuthenticated])
def textmessage(request):
    result = request.session["text"]
    message_obj = Message(result, "content")
    serializer_class = MessageSerializer(message_obj)
    return Response(serializer_class.data)


# def predict(request) -> List[dict]:
#     input_text = request.session.get("text", "")
#     if not input_text:
#         raise ValueError("No input text")
#     masked_text = " ".join(input_text.split(" ")) + " <mask>"
#     predictions = unmasker([masked_text], top_k=20)
#     Prediction.objects.all().delete()
#     filters = ["!!!", "...", ".", "..", "!!", "!"]
#     predictions_filtered = list(
#         filter(lambda x: x["token_str"] not in filters, predictions)
#     )
#     obj_list = [
#         Prediction(prediction=pred["token_str"]) for pred in predictions_filtered[:5]
#     ]
#     print(predictions_filtered[:5])
#     Prediction.objects.bulk_create(obj_list)
