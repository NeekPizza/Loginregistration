from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
# from . import models
from .models import Users
# Create your views here.

def index(request):
    return render(request,'loginregistration/index.html')

def regprocess(request):
    form = request.POST
    response=Users.objects.registration(form)
    print Users.objects.all()
    if not response[0]:
        for error in response[1]:
            messages.add_message(request,messages.INFO,error )
        return redirect('/')
    else:
        id=Users.objects.filter(email=request.POST['email'])[0].id
        request.session['user_id']=id
        return redirect('/success')

def loginprocess(request):
    form = request.POST
    response=Users.objects.login(form)
    if not response[0]:
        for error in response[1]:
            messages.add_message(request,messages.INFO,error )
        return redirect('/')
    else:
        id=Users.objects.filter(email=request.POST['email'])[0].id
        request.session['user_id']=id
        return redirect('/success')

def success(request):
    first_name=(Users.objects.filter(id=request.session['user_id'])[0]).first_name
    context={
    'first_name':first_name
    }
    return render(request, 'loginregistration/success.html',context)

def logout(request):
    request.session.pop('user_id')
    return redirect('/')
