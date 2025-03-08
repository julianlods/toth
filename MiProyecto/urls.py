from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from toth import views  # Importa las vistas de la app 'toth'

urlpatterns = [
    path('admin/', admin.site.urls),  # Usar el admin estándar de Django
    path('', include('toth.urls')),
    path('get_clases/', views.get_clases, name='get_clases'),  # Esto depende de la función get_clases
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
