from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.timezone import now


# Clase personalizada para los usuarios
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        super().save(*args, **kwargs)


# Clase para los profesores
class Profesor(models.Model):
    nombre = models.CharField(max_length=100, default="Profesor genérico")
    descripcion = models.TextField(blank=True, null=True)

    color_header = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text="Color del header en formato HEX (ej: #ff5733)"
    )

    color_footer = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text="Color del fondo del footer en formato HEX (ej: #171d1e)"
    )

    color_footer_text = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text="Color del texto del footer en formato HEX (ej: #ffffff)"
    )

    def __str__(self):
        return self.nombre


# Datos personales asociados a un usuario
class DatosPersonales(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='datos_personales'
    )
    lugar_origen = models.CharField(max_length=100, blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    estilos_musicales_favoritos = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Estilos musicales favoritos"
    )
    profesor_favorito = models.ForeignKey(
        Profesor, on_delete=models.SET_NULL, null=True, blank=True, related_name='alumnos'
    )
    avatar = CloudinaryField('avatar', blank=True, null=True)

    def __str__(self):
        return f"Datos personales de {self.usuario.username if self.usuario else '(sin usuario)'}"


# Categorías de contenido
class CategoriaContenido(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría de contenido"
        verbose_name_plural = "Categorías de contenido"

    def __str__(self):
        return self.nombre


# Contenido asociado a una categoría
class Contenido(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    video_archivo = CloudinaryField('video_archivo', blank=True, null=True)
    archivo_pdf = CloudinaryField('archivo_pdf', blank=True, null=True)
    categoria = models.ForeignKey(
        CategoriaContenido, on_delete=models.SET_NULL, null=True, blank=True, related_name='contenidos'
    )

    def clean(self):
        if self.video_url and self.video_archivo:
            raise ValidationError("No puedes proporcionar una URL de video y un archivo de video al mismo tiempo.")

    def __str__(self):
        return self.titulo


# Clases dictadas por un profesor con contenidos asociados
class Clase(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    contenidos = models.ManyToManyField(Contenido, related_name='clases')
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='clases')

    def __str__(self):
        return self.titulo


class Inscripcion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inscripciones')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    orden = models.PositiveIntegerField(null=True, blank=True, verbose_name="Orden")

    class Meta:
        ordering = ['orden', 'fecha_inscripcion']  # Ordena primero por orden manual, luego por fecha

    def __str__(self):
        return f"{self.usuario.username} - {self.clase.titulo}"


# Registro de clases realizadas por los usuarios
class ClaseRealizada(models.Model):
    ESTADOS_CLASE = [
        ("pendiente", "Pendiente de realizarse"),
        ("realizada", "Realizada"),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="clases_realizadas")
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="realizaciones")
    fecha_realizacion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CLASE, default="pendiente")

    def __str__(self):
        return f"{self.usuario.username} - {self.clase.titulo} ({self.get_estado_display()})"


# Feedback asociado a clases realizadas
class FeedbackUsuario(models.Model):
    clase_realizada = models.OneToOneField(
        ClaseRealizada, on_delete=models.CASCADE, related_name="feedback"
    )
    comentario = models.TextField(blank=True, null=True)
    contenido_adjunto = models.FileField(upload_to="feedback_adjuntos/", blank=True, null=True)
    puntuacion_contenidos = models.JSONField(
        blank=True, null=True, help_text="Debe ser un diccionario con el ID del contenido y su puntuación."
    )

    def clean(self):
        if FeedbackUsuario.objects.filter(clase_realizada=self.clase_realizada).exclude(pk=self.pk).exists():
            raise ValidationError("Ya existe un feedback para esta clase realizada.")

    def save(self, *args, **kwargs):
        if self.puntuacion_contenidos is None or not isinstance(self.puntuacion_contenidos, dict):
            self.puntuacion_contenidos = {}
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback para {self.clase_realizada.clase.titulo} de {self.clase_realizada.usuario.username}"


# Noticias y novedades
class Novedad(models.Model):
    CLASIFICACION_CHOICES = [
        ('general', 'General'),
        ('sos_vos', 'Sos vos'),
    ]

    ESTADO_CHOICES = [
        (True, 'Activa'),
        (False, 'Inactiva'),
    ]

    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    imagen = CloudinaryField('imagen', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    video_archivo = CloudinaryField('video_archivo', blank=True, null=True)
    estado = models.BooleanField(
        choices=ESTADO_CHOICES, 
        default=True, 
        verbose_name="Estado"
    )
    clasificacion = models.CharField(
        max_length=10, choices=CLASIFICACION_CHOICES, default='general', verbose_name='Clasificación'
    )

    def clean(self):
        if self.video and self.video_archivo:
            raise ValidationError("No puedes proporcionar una URL de video y un archivo de video al mismo tiempo.")

    def save(self, *args, **kwargs):
        # Cambiar automáticamente el estado si la fecha ya pasó
        if self.fecha and self.fecha < now().date():
            self.estado = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Novedad #{self.id} ({self.get_clasificacion_display()})"


class Pago(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pagos")
    clase = models.ForeignKey(Clase, on_delete=models.SET_NULL, null=True, blank=True, related_name="pagos")
    metodo = models.CharField(
        max_length=50,
        choices=[('mercado_pago', 'Mercado Pago'), ('transferencia', 'Transferencia')],
        default="mercado_pago"
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('informado', 'Informado'),  
            ('aprobado', 'Aprobado'),
            ('rechazado', 'Rechazado')
        ],
        default='pendiente'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    init_point = models.URLField(blank=True, null=True, verbose_name="URL de MercadoPago")
    comprobante = CloudinaryField('comprobante', blank=True, null=True)

    def __str__(self):
        return f"Pago de {self.usuario.username} - {self.clase.titulo if self.clase else 'Sin clase'} ({self.estado})"



