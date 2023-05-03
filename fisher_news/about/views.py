from django.views.generic.base import TemplateView


class AboutUsView(TemplateView):
    template_name = 'about/us.html'


class ContactView(TemplateView):
    template_name = 'about/contacts.html'
