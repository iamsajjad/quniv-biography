from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from django.conf import settings

from bio.models import Bio
from settings.models import Settings
from settings.forms import SettingsForm
from user.forms import UserRegisterForm

from user.slug import slug

# Create your views here.

@cache_page(0)
def register(request):

    if request.method == 'POST':
        user = UserRegisterForm(request.POST)

        if user.is_valid() and settings.IS_ORG_EMAIL(request.POST['email']):

            user = user.save(commit=False)
            user.is_superuser = False
            user.is_staff = False
            user.save()

            user_settings = SettingsForm()
            user_settings = user_settings.save(commit=False)
            user_settings.user = user
            user_settings.slug = slug(user.email)
            user_settings.save()

            Bio.objects.create(owner=user).save()

            login(request, user)

            return redirect(f'/{user_settings.slug}')
    else:

        return render(request, 'user/register.html')

    return redirect('/')


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
                user_settings = SettingsForm().save(commit=False)
                user_settings.user = user
                user_settings.slug = slug(user.email)
                user_settings.save()

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


@login_required
@cache_page(0)
def signout(request):

    logout(request)

    return render(request, 'user/signin.html')

