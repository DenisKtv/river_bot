from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('us/', views.AboutUsView.as_view(), name='about_us'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
]
