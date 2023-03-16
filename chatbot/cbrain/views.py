from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Chat, ChatHistory
from .forms import UserCreationForm
from .cbrain import Chatbot

# global chatbot instance
chatbot = Chatbot()

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
        try:
            chat = Chat.objects.get(user=request.user)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(user=request.user)

        chat_history = chat.get_history()
        return render(request, 'chat.html', {'chat_history': chat_history})

    def post(self, request):
        user_message = request.POST.get('user_message')
        try:
            chat = Chat.objects.get(user=request.user)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(user=request.user)

        # with transaction.atomic():
        ChatHistory.objects.create(
            chat_session=chat, message=user_message, is_bot=False)

        if request.session.get('chatbot_active', False):
            global chatbot
            chatbot = Chatbot()
            request.session['chatbot_active'] = True

        chatbot_response = chatbot.get_response(user_message)
        ChatHistory.objects.create(
            chat_session=chat, message=chatbot_response, is_bot=True)

        return redirect('chat')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('chat')

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
    global chatbot
    chatbot = Chatbot() # reset chatbot
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
