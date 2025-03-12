from django import forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from .models import Usuario, Inscripcion, Clase, Novedad, DatosPersonales, ClaseRealizada, FeedbackUsuario, Pago
from .forms import UsuarioRegistroForm, EditarDatosPersonalesForm, LoginUsuarioForm, EditarPerfilForm, ContactoForm, ClaseRealizadaForm, FeedbackUsuarioForm, CustomPasswordChangeForm, InformarPagoForm
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from mercadopago import SDK
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
import mercadopago


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        # Autenticar por email o username
        user = authenticate(request, username=username_or_email, password=password)
        if not user:
            try:
                user_obj = Usuario.objects.get(Q(email=username_or_email))
                user = authenticate(request, username=user_obj.username, password=password)
            except Usuario.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect('toth:mis_clases')
        else:
            return render(request, 'toth/login.html', {
                'error_message': 'Usuario o contraseña incorrectos.'
            })

    return render(request, 'toth/login.html')


def index_view(request):
    # Filtrar solo novedades activas
    novedades_generales = Novedad.objects.filter(
        estado=True,
        clasificacion='general'
    ).order_by('-fecha')

    novedades_sos_vos = Novedad.objects.filter(
        estado=True,
        clasificacion='sos_vos'
    ).order_by('-fecha')

    return render(request, 'toth/index.html', {
        'novedades_generales': novedades_generales,
        'novedades_sos_vos': novedades_sos_vos,
    })


def mis_clases_view(request):
    if request.user.is_authenticated:
        inscripciones = Inscripcion.objects.filter(usuario=request.user).select_related('clase', 'clase__profesor')
        clases = [inscripcion.clase for inscripcion in inscripciones]
        clases_realizadas = ClaseRealizada.objects.filter(usuario=request.user)

        # Crear un diccionario con las clases realizadas
        clases_realizadas_dict = {
            clase_realizada.clase.id: clase_realizada for clase_realizada in clases_realizadas
        }

        # Pasar las clases con su estado al contexto
        clases_con_estado = []
        for clase in clases:
            estado = "pendiente"
            fecha_realizacion = None

            if clase.id in clases_realizadas_dict:
                estado = clases_realizadas_dict[clase.id].estado
                fecha_realizacion = clases_realizadas_dict[clase.id].fecha_realizacion

            clases_con_estado.append({
                "clase": clase,
                "estado": estado,
                "fecha_realizacion": fecha_realizacion,
            })

        return render(request, 'toth/mis_clases.html', {
            'clases_con_estado': clases_con_estado,
        })

    return render(request, 'toth/mis_clases.html', {
        'mensaje': 'No tenés clases. Accedé al portal para comenzar a estudiar con tu profesor.',
    })


def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            # Simular envío de correo electrónico
            asunto = f"Consulta de {nombre}"
            cuerpo = f"Mensaje de {nombre} <{email}>:\n\n{mensaje}"
            destinatario = settings.DEFAULT_CONTACT_EMAIL
            send_mail(asunto, cuerpo, email, [destinatario])

            # Pasar el mensaje de éxito al contexto
            return render(request, 'toth/contacto.html', {
                'form': ContactoForm(),
                'success_message': "¡Tu mensaje ha sido enviado con éxito! A la brevedad nos pondremos en contacto."
            })
    else:
        form = ContactoForm()

    return render(request, 'toth/contacto.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        user_form = UsuarioRegistroForm(request.POST)
        datos_form = EditarDatosPersonalesForm(request.POST, request.FILES)

        if user_form.is_valid() and datos_form.is_valid():
            # Guardar el usuario
            usuario = user_form.save()

            # Guardar los datos personales relacionados
            datos_personales = datos_form.save(commit=False)
            datos_personales.usuario = usuario
            datos_personales.save()

            # Autenticar al usuario para obtener el backend
            usuario = authenticate(username=usuario.username, password=request.POST['password1'])

            # Iniciar sesión con el backend explícito
            if usuario is not None:
                login(request, usuario)

            # Redirigir al usuario a su página principal o donde desees
            return redirect('toth:mis_clases')

        else:
            # Pasar mensaje de error al contexto
            return render(request, 'toth/register.html', {
                'user_form': user_form,
                'datos_form': datos_form,
                'error_message': 'Por favor corrige los errores en el formulario.'
            })
    else:
        user_form = UsuarioRegistroForm()
        datos_form = EditarDatosPersonalesForm()

    return render(request, 'toth/register.html', {'user_form': user_form, 'datos_form': datos_form})


@login_required
def clase_detalle_view(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    contenidos = clase.contenidos.all()

    # Verificar si el usuario ya marcó esta clase como realizada
    clase_realizada = ClaseRealizada.objects.filter(usuario=request.user, clase=clase).first()

    return render(request, 'toth/clase_detalle.html', {
        'clase': clase,
        'contenidos': contenidos,
        'clase_realizada': clase_realizada  # Pasamos la variable al template
    })


def logout_view(request):
    logout(request)
    return redirect('toth:index')


@login_required
def perfil_view(request):
    user = request.user
    datos_personales = DatosPersonales.objects.get(usuario=user)

    user_form = EditarPerfilForm(instance=user)
    datos_form = EditarDatosPersonalesForm(instance=datos_personales)
    password_form = CustomPasswordChangeForm(user=user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'contact_form':
            user_form = EditarPerfilForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, '¡Tu información de contacto se ha actualizado con éxito!')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario de contacto.')

        elif form_type == 'personal_form':
            datos_form = EditarDatosPersonalesForm(request.POST, request.FILES, instance=datos_personales)
            if datos_form.is_valid():
                datos_form.save()
                messages.success(request, '¡Tus datos personales se han actualizado con éxito!')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario de datos personales.')

        elif form_type == 'password_form':
            password_form = CustomPasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)  # Mantener la sesión activa
                messages.success(request, '¡Tu contraseña se ha actualizado con éxito!')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario de contraseña.')

    return render(request, 'toth/perfil.html', {
        'user_form': user_form,
        'datos_form': datos_form,
        'password_form': password_form,
    })


@login_required
def marcar_clase_realizada(request, clase_id):
    if request.method == "POST":
        clase = get_object_or_404(Clase, id=clase_id)

        # Registrar o actualizar la clase como realizada
        clase_realizada, created = ClaseRealizada.objects.get_or_create(
            usuario=request.user,
            clase=clase,
            defaults={"estado": "realizada", "fecha_realizacion": now().date()},
        )
        
        if not created:
            # Si ya existe, actualizamos el estado y la fecha
            clase_realizada.estado = "realizada"
            clase_realizada.fecha_realizacion = now().date()
            clase_realizada.save()

        return redirect("toth:feedback_clase", clase_id=clase_id)


@login_required
def feedback_clase(request, clase_id):
    clase_realizada = get_object_or_404(
        ClaseRealizada, clase_id=clase_id, usuario=request.user
    )

    # Obtener o crear el feedback asociado
    feedback, _ = FeedbackUsuario.objects.get_or_create(clase_realizada=clase_realizada)

    # Obtener los contenidos de la clase
    contenidos = clase_realizada.clase.contenidos.all()

    if request.method == "POST":
        form_feedback = FeedbackUsuarioForm(request.POST, request.FILES, instance=feedback)

        if form_feedback.is_valid():
            feedback = form_feedback.save(commit=False)

            # Asegurarse de que puntuacion_contenidos sea un diccionario
            if feedback.puntuacion_contenidos is None or not isinstance(feedback.puntuacion_contenidos, dict):
                feedback.puntuacion_contenidos = {}

            # Actualizar puntuaciones para cada contenido
            for contenido in contenidos:
                field_name = f"puntuacion_contenido_{contenido.id}"
                puntuacion = form_feedback.cleaned_data.get(field_name)
                if puntuacion:
                    feedback.puntuacion_contenidos[str(contenido.id)] = puntuacion

            feedback.save()

            # Marcar la clase como realizada
            clase_realizada.estado = "realizada"
            clase_realizada.fecha_realizacion = now().date()
            clase_realizada.save()

            return redirect("toth:mis_clases")
    else:
        # Pasar dinámicamente los contenidos al formulario
        form_feedback = FeedbackUsuarioForm(instance=feedback)
        for contenido in contenidos:
            field_name = f"puntuacion_contenido_{contenido.id}"
            form_feedback.fields[field_name] = forms.ChoiceField(
                choices=[
                    ("incomprensible", "Incomprensible"),
                    ("muy_facil", "Comprensible pero muy fácil"),
                    ("muy_dificil", "Comprensible pero muy difícil"),
                    ("excelente_mas", "Excelente, quiero más de esto"),
                    ("excelente_poco_interes", "Excelente, pero no me interesa tanto")
                ],
                label=f"Puntuar: {contenido.titulo}",
                widget=forms.RadioSelect,
                required=False
            )

    return render(request, "toth/feedback_form.html", {
        "form_feedback": form_feedback,
        "clase": clase_realizada.clase,
    })


@login_required
def desmarcar_clase_realizada(request, clase_id):
    if request.method == "POST":
        clase_realizada = get_object_or_404(
            ClaseRealizada, clase_id=clase_id, usuario=request.user
        )

        # Eliminar el feedback asociado si existe
        feedback = FeedbackUsuario.objects.filter(clase_realizada=clase_realizada).first()
        if feedback:
            feedback.delete()

        # Actualizar el estado de la clase realizada
        clase_realizada.estado = "pendiente"
        clase_realizada.fecha_realizacion = None
        clase_realizada.save()

        return redirect("toth:mis_clases")


@login_required
def generar_pago(request):
    pagos_pendientes = Pago.objects.filter(usuario=request.user, estado="pendiente")
    pagos_informados = Pago.objects.filter(usuario=request.user, estado="informado")  # 👈 Nuevo estado
    pagos_rechazados = Pago.objects.filter(usuario=request.user, estado="rechazado")
    pagos_aprobados = Pago.objects.filter(usuario=request.user, estado="aprobado")

    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    for pago in pagos_pendientes:
        if pago.estado == "pendiente" and pago.init_point:
            pago.init_point = None
            pago.save()

        if not pago.init_point:
            preference_data = {
                "items": [
                    {
                        "title": f"Pago por {pago.clase.titulo if pago.clase else 'Clase no asignada'}",
                        "quantity": 1,
                        "unit_price": float(pago.monto),
                        "currency_id": "ARS",
                    }
                ],
                "payer": {
                    "email": request.user.email,
                },
                "payment_methods": {
                    "installments": 1,
                },
                "back_urls": {
                    "success": request.build_absolute_uri('/pago-exitoso/'),
                    "failure": request.build_absolute_uri('/pago-fallido/'),
                    "pending": request.build_absolute_uri('/pago-pendiente/')
                },
                "auto_return": "approved",
                "external_reference": str(pago.id),
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response.get("response", {})

            pago.init_point = preference.get("init_point")
            pago.save()

    return render(request, 'toth/pago.html', {
        "pagos_pendientes": pagos_pendientes,
        "pagos_informados": pagos_informados,
        "pagos_rechazados": pagos_rechazados,
        "pagos_aprobados": pagos_aprobados,
    })


def pago_exitoso(request):
    return render(request, 'toth/pago_exitoso.html', {"mensaje": "¡Pago realizado con éxito!"})

def pago_fallido(request):
    return render(request, 'toth/pago_fallido.html', {"mensaje": "El pago no se pudo procesar. Inténtalo nuevamente."})


@login_required
def pago_pendiente(request):
    messages.success(request, "Tu pago ha sido informado y está pendiente de validación.")
    return redirect(reverse("toth:generar_pago") + "#informed")


@csrf_exempt
def get_clases(request):
    usuario_id = request.GET.get('usuario_id')
    if usuario_id:
        clases = Clase.objects.filter(
            id__in=Inscripcion.objects.filter(usuario_id=usuario_id).values_list('clase_id', flat=True)
        )
        clases_data = [{'id': clase.id, 'titulo': clase.titulo} for clase in clases]
        return JsonResponse(clases_data, safe=False)
    return JsonResponse([], safe=False)


def verificar_estado_pago(request, pago_id):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    
    pago = get_object_or_404(Pago, id=pago_id)

    if not pago.init_point:
        messages.error(request, "No hay un enlace de pago para este pago.")
        return HttpResponseRedirect(reverse("admin:toth_pago_changelist"))

    # Buscar el estado en MercadoPago
    response = sdk.payment().search({"external_reference": str(pago.id)})

    if response["status"] == 200 and response["response"]["results"]:
        estado_mp = response["response"]["results"][0]["status"]

        estado_mapeo = {
            "approved": "aprobado",
            "pending": "pendiente",
            "rejected": "rechazado",
            "in_process": "pendiente",
            "cancelled": "rechazado"
        }

        pago.estado = estado_mapeo.get(estado_mp, "pendiente")
        pago.save()
        messages.success(request, f"Estado del pago actualizado a: {pago.estado}")

    else:
        messages.error(request, "No se encontró información sobre este pago en MercadoPago.")

    # 🔹 En vez de redirigir al portal del usuario, volvemos a la lista de pagos en el admin
    return HttpResponseRedirect(reverse("admin:toth_pago_changelist"))


@login_required
def informar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, usuario=request.user)

    if request.method == "POST":
        form = InformarPagoForm(request.POST, request.FILES, instance=pago)

        if form.is_valid():
            pago.comprobante = form.cleaned_data["comprobante"]
            pago.estado = "informado"  # Pasa de "pendiente" a "informado"
            pago.metodo = "transferencia"
            pago.save(update_fields=["comprobante", "estado", "metodo"])  # Solo actualiza estos campos

            # Mensaje de éxito (NO redirecciona)
            messages.success(request, "Tu pago ha sido informado y será revisado pronto.")
            return render(request, "toth/informar_pago.html", {"form": form, "monto": pago.monto, "pago_id": pago.id})

        else:
            messages.error(request, "Hubo un error en el formulario. Verifica los datos.")

    else:
        form = InformarPagoForm(instance=pago)

    return render(request, "toth/informar_pago.html", {
        "form": form,
        "monto": pago.monto,
        "pago_id": pago.id
    })


@login_required
def guardar_monto(request):
    if request.method == "POST":
        request.session["monto"] = request.POST.get("monto", "")
    return HttpResponseRedirect(reverse("toth:informar_pago"))  # Redirige sin mostrar el monto en la URL


def informar_pago_exitoso(request):
    return render(request, "toth/informar_pago_exitoso.html")
