from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation

# Create your views here.

@cache_page(0)
def homepage(request):

    return render(request, 'home/home.html')






@cache_page(0)
def language(request, pagepath):

    if pagepath.startswith('/en/'):
        return HttpResponseRedirect(pagepath.replace('en', 'ar'))
    elif pagepath.startswith('/ar/'):
        return HttpResponseRedirect(pagepath.replace('ar', 'en'))
    else:
        return HttpResponseRedirect('/en/')

