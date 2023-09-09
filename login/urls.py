from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

# app_name = 'login'

urlpatterns = [
    #...
    path('', views.check_auth, name="check"),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('auth', views.login, name="login"),
    path('create', TemplateView.as_view(template_name="login/create.html")),
    # path('student', views.create_student, name="create-student"),
    # path('tutor', views.create_tutor, name="create-tutor"),
]