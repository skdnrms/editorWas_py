"""pySEWas URL Configuration

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
from django.urls import path
from testWas import views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('froala', views.froala, name='froala'),
    url(r'^froala_editor/', include('froala_editor.urls')),
    path('edit', views.edit, name='edit'),
    path('uploadFile', views.upload, name='upload'),
    path('importDoc', views.importDoc, name='importDoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
