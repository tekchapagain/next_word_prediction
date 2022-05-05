from django.db import models

class Prediction(models.Model):
    prediction = models.CharField(max_length=100)
