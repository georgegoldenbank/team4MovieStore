from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import ForgotPasswordForm
from .models import CustomUser

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] ='The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST,error_class=CustomErrorList)
        if form.is_valid():
            #form.save()
            user = form.save(commit=False)
            user.security_question_answer = form.cleaned_data['security_question_answer']
            user.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})



@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})



def forgotPassword(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            security_question_answer = form.cleaned_data["security_question_answer"]
            new_password = form.cleaned_data["new_password"]

            try:
                user = CustomUser.objects.get(username=username, security_question_answer=security_question_answer)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Your password has been successfully updated!")
                return redirect("accounts.login")  # Redirect to login page
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid username or security answer. Please try again.")

    else:
        form = ForgotPasswordForm()

    return render(request, "accounts/forgotPassword.html", {"form": form})