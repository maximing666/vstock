from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models_view import Onedayk

def index(request):
    latest_onedayk_list = Onedayk.objects.order_by('-vdate')[:3]
    template = loader.get_template('vkday/index.html')
    context = {
        'latest_onedayk_list': latest_onedayk_list,
    }
    return HttpResponse(template.render(context, request))