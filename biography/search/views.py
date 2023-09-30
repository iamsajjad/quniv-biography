from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from django.core.paginator import Paginator

from django.shortcuts import redirect, render

from bio.models import Bio
from search.query import text

# Create your views here.

@login_required
@cache_page(0)
def search(request):

    query = request.GET.get('query')

    if query != '' and query != None:
        documents = Bio.objects.filter(text(query))
    else:
        return redirect('documents')

    paginator = Paginator(documents, 25)
    page = request.GET.get('page')
    documents = paginator.get_page(page)

    response = {
        "query": query,
        "documents": documents,
    }

    return render(request, "search/search.html", response)

