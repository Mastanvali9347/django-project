from django.http import JsonResponse
import re
import json

def get_json_data(request):
    """Safely parse JSON body (avoid errors for GET/empty body)."""
    if request.body:
        try:
            return json.loads(request.body)
        except:
            return {}
    return {}

class basicMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/student/":
            print(request.method, "method")
            print(request.path)
        return self.get_response(request)

class signupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/signup/":
            data = get_json_data(request)
            username = data.get("username")
            email = data.get("email")
            dob = data.get("dob")
            password = data.get("pswd")

            # Here you can add validations later
            print("Signup Data:", username, email, dob, password)

        return self.get_response(request)

class SscMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ["/job1/", "/job2/"]:
            ssc_result = request.GET.get("ssc")
            print(ssc_result, 'hello')

            if ssc_result != 'True':
                return JsonResponse(
                    {"error": "You must pass SSC to apply for this job"},
                    status=400
                )

        return self.get_response(request)

class MedicalFitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/job1/":
            medically_fit = request.GET.get("medically_fit")

            if medically_fit != 'True':
                return JsonResponse(
                    {"error": "You are not medically fit for this job"},
                    status=400
                )

        return self.get_response(request)

class AgeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ["/job1/", "/job2/"]:
            try:
                age = int(request.GET.get("age", 17))
            except:
                age = 17

            # Correct age condition (18–25 allowed)
            if age < 18 or age > 25:
                return JsonResponse(
                    {"error": "Age must be between 18 and 25"},
                    status=400
                )

        return self.get_response(request)

class UsernameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/signup/":
            data = get_json_data(request)
            username = data.get("username", "")

            # Empty check
            if not username:
                return JsonResponse({"error": "Username is required"}, status=400)

            # Length check
            if len(username) < 3 or len(username) > 20:
                return JsonResponse(
                    {"error": "Username must contain 3 to 20 characters"},
                    status=400
                )
            # Start and end check
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse(
                    {"error": "Username cannot start or end with . or _"},
                    status=400
                )
            # Allowed characters
            if not re.match(r"^[a-zA-Z0-9._]+$", username):
                return JsonResponse(
                    {"error": "Username can contain letters, numbers, dot, underscore only"},
                    status=400
                )
            # ".." and "__" check
            if ".." in username or "__" in username:
                return JsonResponse(
                    {"error": "Username cannot contain '..' or '__'"},
                    status=400
                )
        return self.get_response(request)
