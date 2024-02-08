"""django_site URL Configuration

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
from django.urls import path, re_path

from twitter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/usuarios$', views.UserController.as_view()),
    re_path(r'^api/login$', views.LoginController.as_view()),
    re_path(r'^api/usuario_detalle/(?P<id>[0-9]+)$', views.UsuarioDetalleController.as_view()),
    re_path(r'^api/publicaciones$', views.PublicacionController.as_view()),
    re_path(r'^api/publicacion/(?P<id>[0-9]+)$', views.PublicacionDetalleController.as_view()),
    re_path(r'^api/usuarios/(?P<id>[0-9]+)/tablon$', views.TablonController.as_view()),
    re_path(r'^api/follower/(?P<id>[0-9]+)$', views.FollowerController.as_view()),
    re_path(r'^api/followers/(?P<id>[0-9]+)$', views.FollowersController.as_view()),
    re_path(r'^api/chat/(?P<id>[0-9]+)$', views.ChatController.as_view()),
]
