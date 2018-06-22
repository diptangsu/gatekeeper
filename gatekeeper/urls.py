from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
import owner.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', owner.views.index, name='index'),
    path('manager/', include('manager.urls')),
    path('scan/', include('scanner.urls')),
    path('owner/', include('owner.urls')),
    path('reception/', include('reception.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
entry
. manager
. scanner
. reception
. owner --> homepage
'''