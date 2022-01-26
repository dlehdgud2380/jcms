from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from account.forms import UserForm

# Create your views here.
def signup(request):
    """
    ## 계정생성하는 함수
    * endpoint: 'account/signup/'
    * function: POST
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            print(username, raw_password, email)

            #user = User.objects.create_user()
            return redirect('index')
    else:
        form = UserForm()

    return render(request, 'account/login.html', {'form': form})