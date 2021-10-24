import bcrypt
from django.shortcuts import render, redirect, reverse
from django.contrib   import messages
from django.db.models import Q

from login.models     import User

def login(request):
    return render(request, 'login/login.html')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect(reverse('homepage'))


def registration_process(request):
    okay = True
    if User.objects.filter(username=request.POST['username']).exists():
        messages.add_message(request, messages.ERROR, 'This username is already registered.')
        okay = False

    if User.objects.filter(email=request.POST['email']).exists():
        messages.add_message(request, messages.ERROR, 'This email address is already registered.')
        okay = False

    if request.POST['password1'] != request.POST['password2']:
        messages.add_message(request, messages.ERROR, 'Passwords do not match.')
        okay = False

    if not okay:
        return redirect(reverse('login'))

    hashed_password = bcrypt.hashpw(request.POST['password1'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create( username = request.POST['username'],
                                email    = request.POST['email'],
                                password = hashed_password
                              )
    request.session['user_id'] = user.id
    return redirect(reverse('homepage'))


def login_process(request):
    if not User.objects.filter(Q(username = request.POST['username']) |
                               Q(email    = request.POST['username'])).exists():
        messages.add_message(request, messages.ERROR, 'Username and/or Password do not match.')
        return redirect(reverse('login'))

    user = User.objects.get(Q(username = request.POST['username']) |
                            Q(email    = request.POST['username']))

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.add_message(request, messages.ERROR, 'Username and/or Password do not match.')
        return redirect(reverse('login'))

    request.session['user_id'] = user.id
    return redirect(reverse('homepage'))
