from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('', lambda r : HttpResponseRedirect ( 'post_corona_lab/index')), #root

    path('admin/', admin.site.urls),
    path('post_corona_lab/', include('post_corona_lab.urls')),
]
