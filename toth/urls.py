from django.urls import path
from . import views  # Importa el módulo completo de vistas
from toth.views import verificar_estado_pago
from .views import informar_pago, guardar_monto

app_name = 'toth'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),  # Ruta para iniciar sesión
    path('register/', views.register_view, name='register'),  # Ruta para registrarse
    path("mis_clases/", views.mis_clases_view, name="mis_clases"),  # Ruta para Mis Clases
    path('clase/<int:clase_id>/', views.clase_detalle_view, name='clase_detalle'),  # Ruta para Detalle de Clase
    path("marcar_clase_realizada/<int:clase_id>/", views.marcar_clase_realizada, name="marcar_clase_realizada"),
    path("feedback_clase/<int:clase_id>/", views.feedback_clase, name="feedback_clase"),
    path('desmarcar_clase_realizada/<int:clase_id>/', views.desmarcar_clase_realizada, name='desmarcar_clase_realizada'),
    path('contacto/', views.contacto_view, name='contacto'),  # Ruta para contacto
    path('perfil/', views.perfil_view, name='perfil'),  # Ruta para el perfil del usuario
    path('logout/', views.logout_view, name='logout'),  # Ruta para cerrar sesión
    path('generar-pago/', views.generar_pago, name='generar_pago'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago-pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('verificar_pago/<int:pago_id>/', verificar_estado_pago, name='verificar_estado_pago'),
    path('api/get-clases/<int:usuario_id>/', views.get_clases, name='get_clases'),
    path("informar-pago/<int:pago_id>/", informar_pago, name="informar_pago"),
    path("informar-pago-exitoso/", views.informar_pago_exitoso, name="informar_pago_exitoso"),
    path("guardar-monto/", guardar_monto, name="guardar_monto"),
]