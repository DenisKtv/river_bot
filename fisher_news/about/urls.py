from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('us/', views.AboutUsView.as_view(), name='us'),
    path('contacts/', views.contacts, name='contacts'),
]
