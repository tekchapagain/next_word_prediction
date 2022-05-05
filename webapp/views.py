from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'nepali.html')
def keyeng(request):
    return render(request,'index.html') 
