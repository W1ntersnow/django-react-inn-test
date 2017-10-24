from django.shortcuts import render
from django.views.generic import TemplateView
from .models import User


def index(request):
    return render(request, 'index.html', {'data': User.objects.all()})


class IndexView(TemplateView):
    template_name = 'main/index.html'
