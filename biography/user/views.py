from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect, render

from django.contrib.auth.models import User

from bio.models import Bio
from settings.models import Settings
from settings.forms import SettingsForm
from user.forms import UserRegisterForm

from .slug import slug

# Create your views here.

@cache_page(0)
def signin(request):

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if not Bio.objects.filter(owner=user).exists():

                # user is created using CLI with out bio object
                Bio.objects.create(owner=user).save()

            if not Settings.objects.filter(user=user).exists():

                # user is created using CLI with out settings object
                settings = SettingsForm().save(commit=False)
                settings.user = user
                settings.slug = slug()
                settings.save()

            login(request, user)

            return redirect('/')
        else:
            return redirect('signin')
    else:
        # get next page
        next_page = request.GET.get('next', '/')

        if User.objects.filter(username=request.user).exists():

            return redirect('/')

        response = {
            'next_page': next_page,
        }

    return render(request, 'user/signin.html', response)


@cache_page(0)
def register(request):

    if request.method == 'POST':
        user = UserRegisterForm(request.POST)
        settings = SettingsForm()

        if user.is_valid():

            user = user.save(commit=False)
            user.is_superuser = False
            user.is_staff = False
            user.save()

            settings = settings.save(commit=False)
            settings.user = user
            settings.slug = slug()
            settings.save()

            Bio.objects.create(owner=user).save()

            login(request, user)

            return redirect(f'/{settings.slug}')
    else:

        return render(request, 'user/register.html')

    return redirect('/')

@login_required
@cache_page(0)
def signout(request):

    logout(request)

    return render(request, 'user/signin.html')

