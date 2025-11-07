from django.http import HttpResponse
from django.http import JsonResponse

def greet(request):
    return HttpResponse("Hello World")

def greet1(request):
    return HttpResponse("Welcome to Django")

def greetinfo(request):
    # data={"name":"mastan", 'age':25, 'city':"hyd"}
    data = {"result":[5,6,7,8,9]}
    return JsonResponse(data, safe=False)