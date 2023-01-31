from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import signupform
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.views.decorators.csrf import csrf_protect

# Create your views here.
def signup(request):
    if request.method=='POST':
       form = signupform(request.POST)
       if form.is_valid():
        form.save()
        return redirect('login')
    else:
        form=signupform()
    return render(request, 'signup/signup.html',{'form':form})
    

# @csrf_protect
def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        
    
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Login failed. Please enter correct credentials.")
            


    else:
        return render(request, 'signup/login.html')


def next(request):
    return render(request, 'signup/next.html')


#     return HttpResponse('handle login')
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('index')


    
