from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import Student


def greet(request):
    return HttpResponse("Hello World")

def greet1(request):
    return HttpResponse("Welcome to Django")

def greetinfo(request):
    # data={"name":"mastan", 'age':25, 'city':"hyd"}
    data = {"result":[5,6,7,8,9]}
    return JsonResponse(data, safe=False)


def dynamicResponse(request):
    name=request.GET.get("name",'kiran')
    city=request.GET.get("city",'hyd')
    
    return HttpResponse(f"hello {name} from {city}")

#to test database connection
def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})


@csrf_exempt
def addStudent(request):
    print(request.method)
    if request.method=='POST':
        data=json.loads(request.body)
        student = Student.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
        )
        return JsonResponse({"status":"success","id":student.id}, status=400)
    return JsonResponse({"error":"use post method"}, status=400)



