"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from basic import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('greet/', views.greet, name='greet'),
    path('greet1/', views.greet1, name='greet1'),
    path('greetinfo/', views.greetinfo, name='greetinfo'),  # ← Missing comma added here
    path('dynamic/', views.dynamicResponse, name='dynamic'),
    path('health/', views.health, name='health'),
    path('add/', views.addStudent, name='add'),

]



#get, post, put, delete

