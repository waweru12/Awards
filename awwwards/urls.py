from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url(r'^$',views.home,name='homePage'),
    url(r'^upload$',views.upload,name='upload'),
    url(r'^ratecontent/(\d+)',views.add_content, name='ratecontent'),
    url(r'^ratedesign/(\d+)',views.add_design, name='ratedesign'),
    url(r'^rateusability/(\d+)',views.add_usability, name='rateusability'),
    url(r'^profile/(\d+)',views.profile,name='profile'),
    url(r'^search/', views.search_results, name='search_results'),



]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)