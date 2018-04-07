"""fundxray URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from fundxray.view import *

urlpatterns = [
    #patterns('',(r'^site_medias/(?P<path>.*)$','django.views.static.serve','document_root':mysite.settings.STATICFILES_DIRS, 'show_indexes': True}),
    url(r'^admin/', admin.site.urls),
    url('list1/$', list1),
    url('show_income/(\d+)/$', show_income),
    url('show_detail/(\d+)/(\d+)/$', show_detail),
]
