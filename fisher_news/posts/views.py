from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.core.paginator import Paginator


# Create your views here.
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
    posts = Post.objects.filter(group=group_news).order_by('pub_date')[:7]
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
