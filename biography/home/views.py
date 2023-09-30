from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation

# Create your views here.

@cache_page(0)
def homepage(request):

    return render(request, 'home/home.html')

@cache_page(0)
def language(request, lang, bio):

    lang = {'ar': 'en',  'en': 'ar'}.get(lang, 'en')
    translation.activate(lang)

    return HttpResponseRedirect(f'/{lang}/bio/{bio}')

