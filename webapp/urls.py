from django.urls import path
from . import views

urlpatterns = [
    path('nepali', views.index, name="nepali"),
    path('', views.keyeng, name="engtonepali"),
]