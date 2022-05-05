from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.listmessage,name = 'typedtext'),
    path('text/', views.textmessage),
    path('predicted/', views.prediction),
]
   