from typing import ItemsView
from rest_framework import serializers
from api.models import Prediction   

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'


class MessageSerializer(serializers.Serializer):
    query = serializers.CharField()
    content = serializers.CharField()


