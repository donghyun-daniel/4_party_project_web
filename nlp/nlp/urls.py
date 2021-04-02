"""nlp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from nlp_proj.views import index
from nlp_proj.views import index2
from nlp_proj.views import upload_view
from nlp_proj.views import lineChart
from nlp_proj.views import lineChart2
from django.conf.urls.static import static
from nlp import settings

#10:54 url 건듬

urlpatterns = [
    path('admin/', admin.site.urls),
    path('firstPage', index, name = 'index'),
    path('firstPageS', index2, name = 'index2'),
    path('', upload_view),
    path('secondPage', lineChart),
    path('secondPageS', lineChart2),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
