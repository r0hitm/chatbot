from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Chat, ChatHistory, Chatbot
from .forms import UserCreationForm


def index(request):
    # if user is logged in, redirect to chat page
    if request.user.is_authenticated:
        return redirect('chat')
    # otherwise, redirect to login page
    return redirect('login')

    # # For testing purposes, redirect to chat page
    # return redirect('chat')


class chat_view(LoginRequiredMixin, View):
    def get(self, request):
        # if the user is not logged in, otherwise 404 in this route
        chat = get_object_or_404(Chat, user=request.user)
        chat_history = chat.get_history()
        return render(request, 'chat.html', {'chat_history': chat_history})

    def post(self, request):
        user_message = request.POST.get('user_message')
        chat = get_object_or_404(Chat, user=request.user)

        with transaction.atomic():
            ChatHistory.objects.create(
                chat_session=chat, message=user_message, is_bot=False)
            chatbot = Chatbot()
            chatbot_response = chatbot.respond(user_message)
            ChatHistory.objects.create(
                chat_session=chat, message=chatbot_response, is_bot=True)

        return redirect('chat')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat')
        else:
            return redirect('signup')
    else:
        return render(request, 'signup.html')
