from django.conf.urls import include
from django.urls import path

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('menu/', include('menu.urls')),
    path('materials/', include('materials.urls')),
    path('rfqs/', include('rfqs.urls')),
    path('quotes/', include('quotes.urls')),
    path('providers/', include('providers.urls')),
    path('admin/', admin.site.urls),
]
