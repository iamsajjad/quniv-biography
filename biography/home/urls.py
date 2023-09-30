
from django.urls import path
from home.views import homepage, language

urlpatterns = (
    path('', homepage, name='homepage'),
    path('language/<str:lang>/<str:bio>/', language, name='language'),
)

