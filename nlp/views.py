from django.shortcuts import render
import sys
from subprocess import run,PIPE

def home(request):
    return render(request,'nlp/index.html')

