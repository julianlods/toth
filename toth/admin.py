from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import reverse, NoReverseMatch
from .models import Usuario, Profesor, CategoriaContenido, Contenido, Clase, Inscripcion, DatosPersonales, Novedad, FeedbackUsuario, ClaseRealizada, Pago
from .forms import PagoForm


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ocultar y desactivar validación solo si el campo existe
        if 'clase' in self.fields:
            self.fields['clase'].required = False
            self.fields['clase'].widget = forms.HiddenInput()

            if self.instance and self.instance.pk:
                usuario = self.instance.usuario
                if usuario:
                    self.fields['clase'].queryset = Clase.objects.filter(
                        id__in=Inscripcion.objects.filter(usuario=usuario).values_list('clase_id', flat=True)
                    )
            elif 'usuario' in self.data:
                try:
                    usuario_id = int(self.data.get('usuario'))
                    self.fields['clase'].queryset = Clase.objects.filter(
                        id__in=Inscripcion.objects.filter(usuario_id=usuario_id).values_list('clase_id', flat=True)
                    )
                except (ValueError, TypeError):
                    self.fields['clase'].queryset = Clase.objects.none()
            else:
                self.fields['clase'].queryset = Clase.objects.none()


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    form = PagoForm
    list_display = ('id', 'usuario', 'metodo', 'monto', 'estado', 'fecha', 'ver_comprobante', 'verificar_estado')
    list_filter = ('estado', 'metodo', 'fecha')
    search_fields = ('id', 'usuario__username', 'usuario__email', 'clase__titulo')
    ordering = ('-fecha',)
    fields = ('id', 'usuario', 'metodo', 'monto', 'estado', 'ver_comprobante')
    readonly_fields = ('id', 'ver_comprobante')

    class Media:
        js = ('admin/js/pago_dynamic_clases.js',)

    def verificar_estado(self, obj):
        try:
            url = reverse('toth:verificar_estado_pago', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" style="padding:5px 10px; background-color:blue; color:white; border-radius:5px; text-decoration:none;">Verificar</a>', 
                url
            )
        except NoReverseMatch:
            return "URL no encontrada"

    def ver_comprobante(self, obj):
        if obj.comprobante:
            return format_html('<a href="{}" target="_blank" style="color: green; font-weight: bold;">Ver Comprobante</a>', obj.comprobante.url)
        return format_html('<span style="color: red;">No adjuntado</span>')
    ver_comprobante.short_description = "Comprobante"

    def save_model(self, request, obj, form, change):
        if 'estado' in form.changed_data:
            if obj.estado == "pendiente":
                obj.init_point = None
            elif obj.estado == "informado":
                obj.estado = "informado"
        super().save_model(request, obj, form, change)

    # Filtrar pagos en el menú lateral del admin
    def changelist_view(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}

        extra_context['custom_menu'] = [
            {
                "title": "Pagos Informados",
                "url": "?estado=informado",
                "description": "Pagos que han sido reportados pero no verificados."
            },
            {
                "title": "Pagos Aceptados",
                "url": "?estado=aceptado",
                "description": "Pagos que han sido aprobados."
            },
            {
                "title": "Pagos Pendientes",
                "url": "?estado=pendiente",
                "description": "Pagos que aún están pendientes de verificación."
            }
        ]
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'profesor', 'descripcion_corta')
    search_fields = ('titulo', 'profesor__nombre')
    list_filter = ('profesor',)
    filter_horizontal = ('contenidos',)  # Facilita la selección de múltiples contenidos

    def descripcion_corta(self, obj):
        return obj.descripcion[:75] + "..." if obj.descripcion and len(obj.descripcion) > 75 else obj.descripcion
    descripcion_corta.short_description = "Descripción"


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clase'].queryset = Clase.objects.all()
        self.fields['clase'].label_from_instance = lambda obj: f"{obj.titulo} - {obj.descripcion[:50]}..." if obj.descripcion else obj.titulo


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clase'].queryset = Clase.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class ClaseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.titulo} - {obj.descripcion[:50]}..." if obj.descripcion else obj.titulo


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'clase_con_descripcion', 'orden', 'fecha_inscripcion')
    list_editable = ('orden',)  # Ahora se puede editar el orden desde el admin
    search_fields = ('usuario__username', 'clase__titulo', 'clase__descripcion')
    list_filter = ('fecha_inscripcion',)
    ordering = ('orden', 'fecha_inscripcion')  # Aplica el orden al mostrar las inscripciones

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['clase'] = ClaseChoiceField(queryset=Clase.objects.all())
        return form

    def clase_con_descripcion(self, obj):
        return f"{obj.clase.titulo} - {obj.clase.descripcion[:50]}..." if obj.clase.descripcion else obj.clase.titulo
    clase_con_descripcion.short_description = "Clase"


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'color_header', 'color_footer', 'color_footer_text')
    search_fields = ('nombre',)
    fields = ('nombre', 'descripcion', 'color_header', 'color_footer', 'color_footer_text')


@admin.register(CategoriaContenido)
class CategoriaContenidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'video_url', 'video_archivo', 'archivo_pdf')
    search_fields = ('titulo',)
    list_filter = ('categoria',)

    def save_model(self, request, obj, form, change):
        # Convertir shorts de YouTube a enlaces normales
        if obj.video_url and "youtube.com/shorts/" in obj.video_url:
            video_id = obj.video_url.split("youtube.com/shorts/")[-1].split("?")[0].split("/")[0]
            obj.video_url = f"https://www.youtube.com/watch?v={video_id}"
        super().save_model(request, obj, form, change)


@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'fecha', 'clasificacion', 'get_estado')
    search_fields = ('descripcion',)
    list_filter = ('fecha', 'clasificacion', 'estado')
    fields = ('descripcion', 'fecha', 'imagen', 'video', 'video_archivo', 'estado', 'clasificacion')

    def get_estado(self, obj):
        return "Activa" if obj.estado else "Inactiva"
    get_estado.short_description = "Estado"


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'get_profesor_favorito', 'lugar_origen', 'edad', 'estilos_musicales_favoritos')
    search_fields = ('usuario__username', 'profesor_favorito__nombre', 'lugar_origen', 'estilos_musicales_favoritos')
    list_filter = ('estilos_musicales_favoritos',)
    ordering = ('usuario',)

    def get_usuario(self, obj):
        return obj.usuario.username if obj.usuario else '(sin usuario)'
    get_usuario.short_description = 'Usuario'

    def get_profesor_favorito(self, obj):
        return obj.profesor_favorito.nombre if obj.profesor_favorito else '(sin profesor)'
    get_profesor_favorito.short_description = 'Profesor favorito'


@admin.register(ClaseRealizada)
class ClaseRealizadaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'clase', 'estado', 'fecha_realizacion')
    search_fields = ('usuario__username', 'clase__titulo')
    list_filter = ('estado', 'fecha_realizacion')

    def usuario(self, obj):
        return obj.usuario.username
    usuario.short_description = "Usuario"

@admin.register(FeedbackUsuario)
class FeedbackUsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_clase', 'get_usuario', 'comentario')
    search_fields = ('clase_realizada__usuario__username', 'clase_realizada__clase__titulo', 'comentario')

    def get_clase(self, obj):
        return obj.clase_realizada.clase.titulo  # Solo muestra el nombre de la clase
    get_clase.short_description = 'Clase'

    def get_usuario(self, obj):
        return obj.clase_realizada.usuario.username
    get_usuario.short_description = 'Usuario'

