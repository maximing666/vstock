from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models_view import Onedayk, Vkdayn

def index(request):
    #按vdate字段倒序，选取3条记录。
    latest_onedayk_list = Onedayk.objects.order_by('-vdate')[:3]
    template = loader.get_template('vkday/index.html')
    context = {
        'latest_onedayk_list': latest_onedayk_list,
    }
    return HttpResponse(template.render(context, request))

def resultndays(request):
    latest_vkdayn_list = Vkdayn.objects.order_by('-vdate')
    template = loader.get_template('vkday/resultndays.html')
    context = {
        'latest_vkdayn_list': latest_vkdayn_list,
    }
    return HttpResponse(template.render(context, request))