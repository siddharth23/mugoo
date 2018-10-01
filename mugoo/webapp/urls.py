from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^create_areas/', create_areas),
    url(r'^search/$', BookList.as_view(), name='search'),
    url(r'', index, name='index'),
]
