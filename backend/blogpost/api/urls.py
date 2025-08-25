"""
URL configuration for blogpost project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# api/urls.py
from django.urls import path

from .views import registerViews, loginView,blog_post_view


urlpatterns = [
    path("createUser/", registerViews.user_list, name="createUser"),
    path("getUser/<int:pk>/", registerViews.user_detail, name="getUserDetail"),
    path("login/", loginView.user_login, name="login_user"),
    path("blog/create/", blog_post_view.blog_list),
    path("blog/<int:id>/", blog_post_view.blog_detail, name="get_blog"),
    path("allblog/", blog_post_view.blog_list_all, name="get_blog"),
    path("protected/", loginView.protected_view),
]


