import json
import os

import requests
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from dotenv import load_dotenv

from .models import Group, Post

load_dotenv()


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    group = Group.objects.all()
    context = {
        'page_obj': page_obj,
        'groups': group,
    }
    return render(request, 'posts/index.html', context)


def post_list(request):
    query = request.GET.get('q')
    if query:
        print(f"query: {query}")
        posts = Post.objects.filter(title__icontains=query)
        for post in posts:
            print(f"title: {post.title}")
    else:
        posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group_news = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group_news).order_by('-pub_date')[:7]
    context = {
        'posts': posts,
        'groups_news': group_news,
    }
    return render(request, 'posts/group_news.html', context)


def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    formatted_text = post.get_formatted_text()
    context = {
        'post': post,
        'formatted_text': formatted_text,
    }
    return render(request, 'posts/news_detail.html', context)


def oauth_callback(request):
    code = request.GET.get('code', '')
    if code:
        return HttpResponse(f"Код авторизации получен: {code}")
    else:
        return HttpResponse("Не удалось получить код авторизации.")


def send_message_to_bot(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone')

        if not any([phone, email, username]):
            response_data = {
                'success': False,
                'message': 'Хотя бы одно из полей (телефон, email, telegram) '
                'должно быть заполнено.'
            }
            return HttpResponse(
                json.dumps(response_data), content_type='application/json'
            )

        telegram_token = os.getenv('ADMIN_TOKEN')
        telegram_chat = os.getenv('MY_CHAT')
        telegram_message = (f'Новое сообщение от пользователя:\nИмя: {name},'
                            f'\nЛогин ТГ: {username},\nEmail: {email},'
                            f'\nТелефон: {phone},\nСообщение: {message}')

        response = requests.get(
            f'https://api.telegram.org/bot{telegram_token}/sendMessage?'
            f'chat_id={telegram_chat}&text={telegram_message}'
        )
        if response.status_code == 200:
            response_data = {
                'status': 'success',
                'message': 'Сообщение успешно отправлено.'
            }
            return HttpResponse(
                json.dumps(response_data), content_type='application/json'
            )
        else:
            response_data = {
                'status': 'error',
                'message': 'Ошибка при отправке сообщения.'
            }
            return HttpResponse(
                json.dumps(response_data), content_type='application/json'
            )
    else:
        response_data = {
            'status': 'error',
            'message': 'Недопустимый метод запроса.'
        }
        return HttpResponse(
            json.dumps(response_data), content_type='application/json'
        )
