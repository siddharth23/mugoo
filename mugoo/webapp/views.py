from django.shortcuts import render
from django.http import JsonResponse
from .models import Area
# Create your views here.
def create_areas(request):
    areas=open(r"C:\Users\mona\code\mugoo\mugoo\webapp\Area.csv",mode="r")
    context1=str(areas.read()).split("\n")
    location={}
    for i in context1:
        if i!="":
            x=i.split(",")
            v=Area(x[1],x[0])
            v.save()
    return JsonResponse(location)