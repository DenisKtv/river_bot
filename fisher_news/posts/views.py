from django.shortcuts import render, get_object_or_404
from .models import Post, Group


# Create your views here.
def index(request):
    posts = Post.objects.order_by('-pub_date')[:7]
    group = Group.objects.all()
    context = {
        'posts': posts,
        'groups': group,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group_news = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group_news).order_by('pub_date')[:7]
    context = {
        'posts': posts,
        'groups_news': group_news,
    }
    return render(request, 'posts/group_news.html', context)


def news_detail(request, pk):
    return render(request, f'Page {pk}')
