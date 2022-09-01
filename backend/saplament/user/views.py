from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages


# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['K_Adi']
        password = request.POST['Sifre']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'oturum açma başarılı')
            return redirect('index')
        else:
            messages.error(request, 'oturum açma başarısız')
            return redirect('index')
    else:
        return render(request, 'user/login.html')


def register(request):
    if request.method == 'POST':

        username = request.POST['K_Adi']
        email = request.POST['email']
        password = request.POST['Sifre']
        rePassword = request.POST['ReSifre']
        if password == rePassword:

            if User.objects.filter(username=username).exists():
                messages.warning(request, 'kullanıcı adı alınmış')
                return redirect('register')
            else:
                if User.objects.filter(email=email, ).exists():
                    messages.warning(request, 'email alınmış')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()

                    messages.success(request, 'kullanıcı oluşturuldu')
                    return redirect('login')




        else:
            print('parolalar eşleşmiyor')
        return redirect('register')
    else:
        return render(request, 'user/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, 'oturum kapatıldı')

    return redirect('index')
