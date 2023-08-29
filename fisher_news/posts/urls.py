from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('post_list/', views.post_list, name='post_list'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts_list'),
    path('oauth_callback/', views.oauth_callback, name='oauth_callback'),
    path(
        'send_message_to_bot/',
        views.send_message_to_bot,
        name='send_message_to_bot'
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
