from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.template import loader, Context, RequestContext
from miscelanea.models import Persona
from miscelanea.forms import LoginForm, PersonaForm

@login_required(login_url='/login/')
def home(request):    
    template = loader.get_template("home.html")
    context = RequestContext(request)
    return HttpResponse({template.render(context)})
    
def log_in(request):
    form = LoginForm()
    template = loader.get_template("login.html")
    context = RequestContext(request,{'login_form':form})
    context.update(csrf(request))
    return HttpResponse({template.render(context)})

@login_required(login_url='/login/')
def log_out(request):
    logout(request)
    return render_to_response('logout.html', context_instance=RequestContext(request))

def validar_usuario(request):
    htmldoc=None
    if request.POST:
        datos=LoginForm(request.POST)
        if datos.is_valid():
            user=datos.cleaned_data['usuario']
            passw=datos.cleaned_data['password']
            usuario=authenticate(username=user,password=passw)
            if usuario is not None:
                login(request,usuario)
                htmldoc="home.html"
            else:
                htmldoc="login_error.html"
        else:
            htmldoc="login.html"
    else:
        return HttpResponseRedirect('/')
    template = loader.get_template(htmldoc)
    context = RequestContext(request)
    context.update(csrf(request))
    return HttpResponse({template.render(context)})

@login_required(login_url='/login/')
def nuevo_usuario(request):
    form = PersonaForm()
    template = loader.get_template("nuevo_usuario.html")
    context = RequestContext(request,{'newuser_form':form})
    return HttpResponse({template.render(context)})

def crear_usuario(request):
    if request.POST:
        datos=PersonaForm(request.POST)
        if datos.is_valid():
            user=datos.cleaned_data['username']
            passw=datos.clean_password2()
            user = User(username=user,password=passw)
            user.set_password(passw)
            user.save()
            datos.save();
            return HttpResponseRedirect('/')
        else:
            return render_to_response('login_error.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/nuevo_usuario/')

