from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from basic.models import StudentNew, Users
import json
import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def greet(request):
    return HttpResponse("Hello World")


def greet1(request):
    return HttpResponse("Welcome to Django")


def greetinfo(request):
    data = {"result": [5, 6, 7, 8, 9]}
    return JsonResponse(data, safe=False)


def dynamicResponse(request):
    name = request.GET.get("name", 'kiran')
    city = request.GET.get("city", 'hyd')
    return HttpResponse(f"hello {name} from {city}")


def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status": "ok", "db": "connected"})
    except Exception as e:
        return JsonResponse({"status": "error", "db": str(e)})


@csrf_exempt
def addStudent(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student = StudentNew.objects.create(
            name=data.get('name'),
            age=data.get("age"),
            email=data.get("email")
        )
        return JsonResponse({"status": "success", "id": student.id}, status=200)

    elif request.method == "GET":
        result = list(StudentNew.objects.values())
        return JsonResponse({"status": "ok", "data": result}, status=200)

    elif request.method == "PUT":
        data = json.loads(request.body)
        ref_id = data.get("id")
        new_email = data.get("email")

        existing_student = StudentNew.objects.get(id=ref_id)
        existing_student.email = new_email
        existing_student.save()

        updated_data = StudentNew.objects.filter(id=ref_id).values().first()
        return JsonResponse({"status": "data updated successfully", "updated_data": updated_data}, status=200)

    elif request.method == "DELETE":
        data = json.loads(request.body)
        ref_id = data.get("id")

        deleted_data = StudentNew.objects.filter(id=ref_id).values().first()
        StudentNew.objects.get(id=ref_id).delete()

        return JsonResponse({
            "status": "success",
            "message": "student record deleted successfully",
            "deleted_data": deleted_data
        }, status=200)

    return JsonResponse({"error": "use POST method"}, status=400)


def job1(request):
    return JsonResponse({"message": "you have successfully applied for job1"}, status=200)


def job2(request):
    return JsonResponse({"message": "you have successfully applied for job2"}, status=200)

@csrf_exempt
def signup_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    # Safely load JSON
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        return JsonResponse({"error": "Invalid or empty JSON body"}, status=400)

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validate fields
    if not username or not email or not password:
        return JsonResponse({"error": "username, email, password required"}, status=400)

    if Users.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    if Users.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)

    user = Users(username=username, email=email)
    user.set_password(password)
    user.save()

    return JsonResponse({"message": "Signup successful"}, status=200)

@csrf_exempt
def login_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=400)
    try:
        if request.body:
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
    except:
        data = request.POST
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return JsonResponse({"error": "username and password required"}, status=400)
    try:
        user = Users.objects.get(username=username)
        issued_at = datetime.now(tz=ZoneInfo("Asia/Kolkata"))
    except Users.DoesNotExist:
        return JsonResponse({"error": "Invalid username or password"}, status=400)
    if not user.check_password(password):
        return JsonResponse({"error": "Invalid username or password"}, status=400)
    payload = {"id": user.id,"username": user.username,"email": user.email}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return JsonResponse({"message": "Login successful", "token": token})

@csrf_exempt
def check(request):
    hashed = "pbkdf2_sha256$870000$rLU1LPQJXTtzz3O3Av6mk6$1JmClQdhTgDVlC7PP+i7HZdIxVGRmTjLPkyXOTbNzM4="
    x = Users.check_password(Users, "12345")
    return JsonResponse({"status": "success", "data": x}, status=200)
