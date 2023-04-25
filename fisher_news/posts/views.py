from django.shortcuts import render
from .models import Post


# Create your views here.
def index(request):
    posts = Post.objects.order_by('-pub_date')[:6]
    context = {
        'post': posts,
    }
    return render(request, 'index.html', context)


def news_detail(request, pk):
    return render(request, f'Page {pk}')
