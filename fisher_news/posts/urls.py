from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
