from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


@login_required(login_url="/login/")
def index(request):
    if request.method == "POST":
        print("Received data " + request.POST["textmessage"])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(
            text=request.POST["textmessage"],
            chat=myChat,
            author=request.user,
            receiver=request.user,
        )
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, "chat/index.html", {"messages": chatMessages})


def login_view(request):
    redirect = request.GET.get("next")
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get("redirect"))
        else:
            return render(
                request,
                "auth/login.html",
                {"wrongPassword": True, "redirect": redirect},
            )

    return render(request, "auth/login.html", {"redirect": redirect})


# Create your views here.
def register_view(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/chat/")
    else:
        form = RegisterForm()

    return render(response, "auth/register.html", {"form": form})
