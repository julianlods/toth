from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Usuario, DatosPersonales, FeedbackUsuario, ClaseRealizada, Pago, Inscripcion, Clase


class UsuarioRegistroForm(UserCreationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Recordá que va a ser tu alias dentro del sitio."
    )
    email = forms.EmailField(
        required=True,
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text=""
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Debe contener al menos 8 caracteres."
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Reingresá la misma contraseña."
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class LoginUsuarioForm(forms.Form):
    username = forms.CharField(
        label="Usuario o Correo Electrónico",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Ingrese su nombre de usuario o correo."
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Ingrese su contraseña."
    )


class EditarDatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = ['lugar_origen', 'edad', 'estilos_musicales_favoritos', 'profesor_favorito', 'avatar']
        widgets = {
            'lugar_origen': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estilos_musicales_favoritos': forms.TextInput(attrs={'class': 'form-control'}),
            'profesor_favorito': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'lugar_origen': 'Lugar de Origen',
            'edad': 'Edad',
            'estilos_musicales_favoritos': 'Estilos Musicales Favoritos',
            'profesor_favorito': 'Profesor Favorito',
            'avatar': 'Avatar',
        }
        help_texts = {
            'lugar_origen': 'Ingresá tu lugar de origen. Por ejemplo, Buenos Aires, Argentina.',
            'edad': 'Especificá tu edad en años, si querés.',
            'estilos_musicales_favoritos': 'Ingresá tus estilos musicales preferidos. Por ejemplo, rock, metal, jazz, etc.',
            'profesor_favorito': 'Seleccioná tu profesor favorito.',
            'avatar': 'Subí una imagen para tu avatar (opcional).',
        }


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
        help_texts = {
            'first_name': 'Ingrese su primer nombre.',
            'last_name': 'Ingrese su apellido.',
            'email': 'Proporcione una dirección de correo válida.',
        }


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre'}),
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo electrónico'}),
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje aquí', 'rows': 4}),
    )


class ClaseRealizadaForm(forms.ModelForm):
    class Meta:
        model = ClaseRealizada
        fields = ["fecha_realizacion"]
        widgets = {
            "fecha_realizacion": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
        labels = {
            "fecha_realizacion": "Fecha de Realización",
        }


# Opciones de puntuación
PUNTUACION_CHOICES = [
    ('incomprensible', 'Incomprensible'),
    ('muy_facil', 'Comprensible pero muy fácil'),
    ('muy_dificil', 'Comprensible pero muy difícil'),
    ('excelente_interes', 'Excelente, quiero más de esto'),
    ('excelente_no_interes', 'Excelente, pero no me interesa tanto'),
]

class FeedbackUsuarioForm(forms.ModelForm):
    class Meta:
        model = FeedbackUsuario
        fields = ['comentario', 'contenido_adjunto']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contenido_adjunto': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'comentario': 'Comentario General',
            'contenido_adjunto': 'Envía un video de tu progreso al profesor',
        }

    def __init__(self, *args, **kwargs):
        # Capturar la clase para la cual se está generando el feedback
        self.clase = kwargs.pop('clase', None)
        super().__init__(*args, **kwargs)

        # Agregar campos dinámicos para cada contenido
        if self.clase:
            for contenido in self.clase.contenidos.all():
                field_name = f"puntuacion_contenido_{contenido.id}"
                self.fields[field_name] = forms.ChoiceField(
                    choices=PUNTUACION_CHOICES,
                    label=contenido.titulo,
                    widget=forms.RadioSelect,
                )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=""
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Debe contener al menos 8 caracteres."
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Reingresá la misma contraseña."
    )


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Verificar si estamos editando un objeto existente
        if self.instance and self.instance.pk:
            usuario = self.instance.usuario
            if usuario:
                self.fields['clase'].queryset = Clase.objects.filter(
                    id__in=Inscripcion.objects.filter(usuario=usuario).values_list('clase_id', flat=True)
                )
            else:
                self.fields['clase'].queryset = Clase.objects.none()
        elif 'usuario' in self.data:  # Si se pasa el usuario desde el formulario
            try:
                usuario = Usuario.objects.get(pk=self.data.get('usuario'))
                self.fields['clase'].queryset = Clase.objects.filter(
                    id__in=Inscripcion.objects.filter(usuario=usuario).values_list('clase_id', flat=True)
                )
            except Usuario.DoesNotExist:
                self.fields['clase'].queryset = Clase.objects.none()
        else:
            # Si es un formulario nuevo, vaciar las opciones de clase
            self.fields['clase'].queryset = Clase.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        clase = cleaned_data.get('clase')

        # Validar que la clase pertenece al usuario seleccionado
        if usuario and clase:
            clases_permitidas = Clase.objects.filter(
                id__in=Inscripcion.objects.filter(usuario=usuario).values_list('clase_id', flat=True)
            )
            if clase not in clases_permitidas:
                raise forms.ValidationError({
                    'clase': "La clase seleccionada no está asociada al usuario seleccionado."
                })
        return cleaned_data


class InformarPagoForm(forms.ModelForm):
    monto = forms.DecimalField(
        required=False,  # 👈 Ahora NO es obligatorio
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Ingresa un monto diferente'})
    )

    class Meta:
        model = Pago
        fields = ['monto', 'comprobante']

