from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from toth import views  # Importa las vistas de la app 'toth'

urlpatterns = [
    path('admin/', admin.site.urls),  # Usar el admin estándar de Django
    path('', include('toth.urls')),
    path('get_clases/', views.get_clases, name='get_clases'),  # Esto depende de la función get_clases
]

# Forzar Django a servir archivos media
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
