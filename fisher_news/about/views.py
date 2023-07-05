from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutUsView(TemplateView):
    template_name = 'about/us.html'


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = 'Новое сообщение от пользователя'
        message = f'Имя: {name}\nEmail: {email}\nСообщение: {message}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [from_email]

        send_mail(subject, message, from_email, recipient_list)

        return HttpResponse('Сообщение успешно отправлено!')

    return render(request, 'about/contacts.html')
