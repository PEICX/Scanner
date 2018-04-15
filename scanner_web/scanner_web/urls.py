"""scanner_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from myapp.views import *

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^scan$', ScanView.as_view(), name="scan"),
    url(r'^about$', AboutView.as_view(), name="about"),
    url(r'^help$', HelpView.as_view(), name="help"),

]



# 全局404界面
handler404 = page_not_found
handler500 = page_error
handler403 = permission_denied