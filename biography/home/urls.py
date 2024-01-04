
from django.urls import path
from home.views import homepage, language

urlpatterns = (
    path('', homepage, name='homepage'),
    path('language/<path:pagepath>', language, name='language'),
)

