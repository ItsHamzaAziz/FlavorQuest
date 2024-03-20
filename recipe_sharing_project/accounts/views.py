from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return render(request, 'accounts/register.html', {
                        'title': 'Register | FlavorQuest',
                        'data': True,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'username': username,
                        'password': password,
                        'password2': password2,
                    })
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return render(request, 'accounts/register.html', {
                        'title': 'Register | FlavorQuest',
                        'data': True,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'username': username,
                        'password': password,
                        'password2': password2,
                    })
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                    user.save()
                    
                    login(request, user)

                    return redirect('home')
                    
            else:
                messages.info(request, 'Passwords are not same')
                return render(request, 'accounts/register.html', {
                        'title': 'Register | FlavorQuest',
                        'data': True,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'username': username,
                        'password': password,
                        'password2': password2,
                })

        return render(request, 'accounts/register.html', {
            'title': 'Register | FlavorQuest',
            'data': False
        })
    except:
        messages.info('An error ocurred')
        return render('register')


def log_in(request):
    try:
        if request.method == 'POST':
            user_input = request.POST['user_input']
            password = request.POST['password']

            if User.objects.filter(username=user_input).exists():
                user = authenticate(username=user_input, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'Incorrect Password')
                    return render(request, 'accounts/login.html', {
                            'title': 'Register | FlavorQuest',
                            'data': True,
                            'user_input': user_input,
                            'password': password,
                    })
            elif User.objects.filter(email=user_input).exists():
                user = User.objects.get(email=user_input)
                user_name = user.username
                user = authenticate(username=user_name, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'Incorrect Password')
                    return render(request, 'accounts/login.html', {
                            'title': 'Register | FlavorQuest',
                            'data': True,
                            'user_input': user_input,
                            'password': password,
                    })
            else:
                messages.info(request, 'Invalid Username or Email')
                return render(request, 'accounts/login.html', {
                        'title': 'Register | FlavorQuest',
                        'data': True,
                        'user_input': user_input,
                        'password': password,
                })

        return render(request, 'accounts/login.html', {
            'title': 'Login | FlavorQuest',
            'data': False
        })
    except:
        messages.info('An error ocurred')
        return render('login')


@login_required
def log_out(request):
    try:
        logout(request)
        return redirect('home')
    except:
        return redirect('home')


@login_required
def account_details(request):
    try:
        return render(request, 'accounts/accountdetails.html', {
            'title': 'Account Details',
            'user': request.user,
            'data':False
        })
    except:
        return redirect('home')


@login_required
def edit_account(request):
    try:
        user = request.user

        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(username=username).exists():
                    if user.username != username:
                        messages.info(request, 'Username already exists')
                        return render(request, 'accounts/register.html', {
                            'title': 'Register | FlavorQuest',
                            'data': True,
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'username': username,
                            'password': password,
                            'password2': password2,
                        })
                    elif User.objects.filter(email=email).exists():
                        if user.email != email:
                            messages.info(request, 'Email already exists')
                            return render(request, 'accounts/register.html', {
                                'title': 'Register | FlavorQuest',
                                'data': True,
                                'first_name': first_name,
                                'last_name': last_name,
                                'email': email,
                                'username': username,
                                'password': password,
                                'password2': password2,
                            })
                        else:
                            user.first_name = first_name
                            user.last_name = last_name
                            user.email = email
                            user.username = username
                            user.set_password(password)
                            user.save()

                            login(request, user)
                            messages.info(request, 'Account Updated')
                            return redirect('account_details')
                    else:
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = email
                        user.username = username
                        user.set_password(password)
                        user.save()

                        login(request, user)
                        messages.info(request, 'Account Updated')
                        return redirect('account_details')
                elif User.objects.filter(email=email).exists():
                    if user.email != email:
                        messages.info(request, 'Email already exists')
                        return render(request, 'accounts/register.html', {
                            'title': 'Register | FlavorQuest',
                            'data': True,
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'username': username,
                            'password': password,
                            'password2': password2,
                        })
                    else:
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = email
                        user.username = username
                        user.set_password(password)
                        user.save()

                        login(request, user)
                        messages.info(request, 'Account Updated')
                        return redirect('account_details')
                else:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.username = username
                    user.set_password(password)
                    user.save()

                    login(request, user)
                    messages.info(request, 'Account Updated')
                    return redirect('account_details')
                
            else:
                messages.info(request, 'Passwords are not same')
                return render(request, 'accounts/register.html', {
                        'title': 'Register | FlavorQuest',
                        'data': True,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'username': username,
                        'password': password,
                        'password2': password2,
                })

        return render(request, 'accounts/editaccount.html', {
            'title': 'Edit Account',
            'user': user,
        })
    except:
        return redirect('home')



