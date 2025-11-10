from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import Student, StudentNew


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

    if request.method == 'POST':
        data = json.loads(request.body)
        student = StudentNew.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
        )
        return JsonResponse({"status": "success", "id": student.id}, status=201)

    elif request.method == 'GET':
        result = StudentNew.objects.all().values()
        return JsonResponse({"status": "success", "data": list(result)}, status=200)

    elif request.method == 'PUT':
        if not request.body:
            return JsonResponse({"error": "empty request body"}, status=400)

        data = json.loads(request.body)
        ref_id = data.get('id')
        new_email = data.get('email')

        if not ref_id or not new_email:
            return JsonResponse({"error": "id and email are required"}, status=400)

        student_qs = StudentNew.objects.filter(id=ref_id)
        if not student_qs.exists():
            return JsonResponse({"error": "no student found with given id"}, status=404)

        student = student_qs.first()
        student.email = new_email
        student.save()

        updated = StudentNew.objects.filter(id=ref_id).values().first()
        return JsonResponse({"status": "data updated successfully", "data": updated}, status=200)

    elif request.method == 'DELETE':
        if not request.body:
            return JsonResponse({"error": "empty request body"}, status=400)

        data = json.loads(request.body)
        ref_id = data.get('id')

        if not ref_id:
            return JsonResponse({"error": "id is required"}, status=400)

        deleting_data = StudentNew.objects.filter(id=ref_id).values().first()
        if not deleting_data:
            return JsonResponse({"error": "no student found with given id"}, status=404)

        StudentNew.objects.filter(id=ref_id).delete()
        return JsonResponse({"status": "data deleted successfully", "data": deleting_data}, status=200)

    return JsonResponse({"error": "invalid method"}, status=400)