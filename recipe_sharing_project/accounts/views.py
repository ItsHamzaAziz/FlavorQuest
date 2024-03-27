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

            # If both passwords are same
            if password == password2:
                # If username already exists
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
                # If email is already in use or exists (as we want to have unique email for each account)
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
                    
                    login(request, user)    # Logging in user as soon as their account is created and redirecting them to home page

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
        messages.info('An error ocurred')   # If error occurs at any stage, user is redirected to register page
        return redirect('register')


def log_in(request):
    try:
        if request.method == 'POST':
            user_input = request.POST['user_input']
            password = request.POST['password']

            # If username exists to check if username entered is valid or not
            if User.objects.filter(username=user_input).exists():
                user = authenticate(username=user_input, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'Incorrect Password')    # If username exists and user is None then surely password is incorrect
                    return render(request, 'accounts/login.html', {
                            'title': 'Register | FlavorQuest',
                            'data': True,
                            'user_input': user_input,
                            'password': password,
                    })
            # Checking if entered email exists as user can user can use either email or username to login
            elif User.objects.filter(email=user_input).exists():
                user = User.objects.get(email=user_input)
                user_name = user.username   # As we need username to use authenticate function so we get that username from that specific user
                user = authenticate(username=user_name, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'Incorrect Password')    # If email exists and user is None then surely password is incorrect
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
        messages.info('An error ocurred')   # If any error is encountered during login process, then redirect to login page with error message
        return redirect('login')


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
                    # If entered username is different from the one user is already using
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
                        # If entered email is different from the one user is already using
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

                            login(request, user)    # On changing password user is automatically logged out so we are logging user in again
                            messages.info(request, 'Account Updated')
                            return redirect('account_details')
                    else:
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = email
                        user.username = username
                        user.set_password(password)
                        user.save()

                        login(request, user)    # On changing password user is automatically logged out so we are logging user in again
                        messages.info(request, 'Account Updated')
                        return redirect('account_details')
                elif User.objects.filter(email=email).exists():
                    # If entered email is different from the one user is already using
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

                        login(request, user)    # On changing password user is automatically logged out so we are logging user in again
                        messages.info(request, 'Account Updated')
                        return redirect('account_details')
                else:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.username = username
                    user.set_password(password)
                    user.save()

                    login(request, user)    # On changing password user is automatically logged out so we are logging user in again
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



