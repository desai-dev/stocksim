from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from portfolio.models import Cash

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            #log user in
            login(request, user)
            user_cash = Cash(cash=1000, owner=request.user)
            user_cash.save()
            return redirect('index')
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'signup.html', context=context)

def login_view(request):
    if request.method =='POST':
        form = AuthenticationForm(data = request.POST)

        if form.is_valid():
            #log user in
            user = form.get_user()
            login(request, user)
            
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form
    }
    return render(request, 'login.html', context=context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')