from django.urls import path, include

from custom_auth import views

urlpatterns = [
    path('signup/', views.RegistrationView.as_view(), name='signup'),
]