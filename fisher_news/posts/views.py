from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def news_detail(request, pk):
    return render(request, f'Page {pk}')
