from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from Register_Page.forms import CreateUser

# Create your views here.


def register(request):
    forms = CreateUser()
    if request.method == 'POST':
        forms = CreateUser(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('')
    ctx = {'forms': forms}
    return render(request, 'Register.html', ctx)


def home(request):
    return render(request, 'Home.html')
