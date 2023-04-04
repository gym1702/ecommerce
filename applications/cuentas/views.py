from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
#
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage



from .forms import RegistrationForm
from .models import Account


#
def registro(request):
    #Registrar usuario
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #funcion para separar el correo
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                               email=email, username=username, password=password)
            user.phone = phone
            user.save()

            #Enviar correo de activacion a usuario
            current_site = get_current_site(request)
            mail_subject = 'Por favor activa tu cuenta en ecommerce'
            body = render_to_string('cuentas/verificar_correo.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()


            #messages.success(request, 'El registro ha sido creado correctamente')
            #return redirect('cuentas_app:registro')

            return redirect('/login/?command=verification&email='+email)
    
    context = {
        'form': form
    }



    return render(request, 'cuentas/registro.html', context)


#
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Ha iniciado sesión exitosamente')
            return redirect('cuentas_app:dashboard')
        else:
            messages.error(request, 'El usuario o contraseña son incorrectas')
            return redirect('cuentas_app:login')

    return render(request, 'cuentas/login.html')


#
@login_required(login_url='cuentas_app:login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Ha cerrado su sesión correctamente')

    return redirect('cuentas_app:login')


#
def activar(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Felicidades, tu cuenta ha sido activada con éxito!')
        return redirect('cuentas_app:login')
    else:
        messages.error(request, 'La activacion ha sido invalida')
        return redirect('cuentas_app:registro')



#
@login_required(login_url='cuentas_app:login')
def dashboard(request):

    return render(request, 'cuentas/dashboard.html')



#
def passwordOlvidado(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Resetear password'
            body =  render_to_string('cuentas/reset_passsword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            messages.success(request, 'Se ha enviado un email para resetear su password')
            return redirect('cuentas_app:login')
        
        else:
            messages.error(request, 'No existe el correo proporcionado')
            return redirect('cuentas_app:passwordOlvidado')

    return render(request, 'cuentas/password_olvidado.html')



#
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Por favor escriba su nueva contraseña')
        return redirect('cuentas_app:resetPassword')

    else:
        messages.error(request, 'El link ha expirado')
        return redirect('cuentas_app:login')
    


#
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()

            messages.success(request, 'Su contraseña ha sido cambiada exitosamente!')
            return redirect('cuentas_app:login')
        
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('cuentas_app:resetPassword')
    
    else:
        return render(request, 'cuentas/resetPassword.html')