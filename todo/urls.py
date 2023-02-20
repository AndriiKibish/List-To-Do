"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from todo_app.views import signup_user, current_todo, logout_user, home, login_user, create_todo,\
    view_todo, complete_todo, delete_todo, completed_todo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', signup_user, name='signup_user'),
    path('logout/', logout_user, name='logout_user'),
    path('login/', login_user, name='login_user'),
    path('current/', current_todo, name='current_todo'),
    path('completed/', completed_todo, name='completed_todo'),
    path('create/', create_todo, name='create_todo'),
    path('todo/<int:todo_pk>/', view_todo, name='view_todo'),
    path('todo/<int:todo_pk>/complete_todo/', complete_todo, name='complete_todo'),
    path('todo/<int:todo_pk>/delete_todo/', delete_todo, name='delete_todo'),

]