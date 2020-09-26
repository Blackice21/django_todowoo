"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from todo import views

urlpatterns = [
    # home page and admin page
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    # user authentication paths
    path('signup/', views.signupuser, name="signupuser"),
    path('currenttodos/logout/', views.logout_view, name='logoutuser'),
    path('login/', views.login_view, name='loginuser'),
    # todo related paths
    path('currenttodos/', views.currenttodos, name="currenttodos"),
    path('completedtodos/', views.completedtodos, name="completedtodos"),
    path('create/', views.create, name='createtodo'),
    # details on each todo object
    path('todo/<int:todo_key>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_key>/completed', views.completed, name='completed'),
    path('todo/<int:todo_key>/delete', views.deletetodo, name='deletetodo'),
]
