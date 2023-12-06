from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from settings.models import Settings
from bio.models import Bio
from link.models import Link
from publication.models import Publication

from bio.forms import BioForm

# Create your views here.

# @login_required
def mainpage(request):

    if request.user.is_anonymous:
        return redirect('signin')

    settings = get_object_or_404(Settings, user=request.user)

    return redirect('biopage', slug=settings.slug)

# @login_required
def biopage(request, slug):

    settings = get_object_or_404(Settings, slug=slug)
    bio = Bio.objects.filter(owner=settings.user)

    if len(bio) == 0:
        # (request user == bio owner) then can edit bio data
        if request.user == bio.owner:
            return redirect('edit', slug=settings.slug)
        else:
            return redirect('error404')
    else:
        bio = bio[0]

    # footer status informations
    status = {'bios':Bio.objects.count(),
              'links' : Link.objects.count(),
              'publications' : Publication.objects.count(),
    }

    response = {
        'biopage': True,
        'settings': settings,
        'bio': bio,
        'status': status,
    }

    return render(request, 'bio.html', response)

@login_required
def edit(request, slug):

    settings = get_object_or_404(Settings, slug=slug)
    bio = Bio.objects.get(owner=settings.user)

    # to edit bio the user must be `superuser` or `owner`
    authorized = request.user.is_superuser or request.user == bio.owner

    if request.method == 'POST' and authorized:

        bio = BioForm(request.POST, request.FILES, instance=bio)

        if bio.is_valid():

            bio.save()

        return redirect('edit', slug=settings.slug)

    else:
        if authorized:

            # footer status informations
            status = {'bios':Bio.objects.count(),
                      'links' : Link.objects.count(),
                      'publications' : Publication.objects.count(),
            }

            response = {
                'editpage': True,
                'settings': settings,
                'bio': bio,
                'status': status,
            }
            return render(request, 'edit_bio.html', response)
    return redirect(f'{slug}')

