from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('core.urls')),
    path('', RedirectView.as_view(pattern_name='event_list')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
