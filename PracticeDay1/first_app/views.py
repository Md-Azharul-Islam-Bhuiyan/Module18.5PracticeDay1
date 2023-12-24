from django.shortcuts import render, redirect
from first_app.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            messages.success(request,'Account Created Successfully')
            register_form.save()
            return redirect('register')
    else:
        register_form = RegisterForm()
    return render(request,'register.html', {'form': register_form})


def user_login(request):
    if request.method == 'POST':
        user_form = AuthenticationForm(request= request, data = request.POST)
        if user_form.is_valid():
            user_name = user_form.cleaned_data['username']
            user_pass = user_form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully')
                return redirect('profile')
            else:
                messages.success(request, 'Login Information Incorrect')
                return redirect('login')
    else:
        user_form = AuthenticationForm(request= request, data = request.POST)
    return render(request, 'login.html', {'form': user_form})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user':request.user})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user,data=request.POST)
        if form.is_valid():
            messages.success(request,'Password Updated Successfully')
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
       form = SetPasswordForm(user=request.user)
    return render(request,'changePass.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request,'Logged Out Successfully')
    return redirect('homepage')