from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
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
    '''Home page'''
    # if user is logged in, redirect to chat page
    if request.user.is_authenticated:
        return redirect('chat')
    return redirect('login')    # otherwise, redirect to login page


class chat_view(LoginRequiredMixin, View):
    '''Chat page'''

    def get(self, request):   # get request
        # get chat session for user, and render chat page
        try:
            chat = Chat.objects.get(user=request.user)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(user=request.user)

        chat_history = chat.get_history()
        return render(request, 'chat.html', {'chat_history': chat_history})

    def post(self, request):  # post request
        user_message = request.POST.get('user_message')

        # get chat session for user
        try:
            chat = Chat.objects.get(user=request.user)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(user=request.user)

        # save user message to database
        ChatHistory.objects.create(
            chat_session=chat, message=user_message, is_bot=False)

        # get chatbot response and save it to database
        chatbot_response = chatbot.get_response(user_message)
        ChatHistory.objects.create(
            chat_session=chat, message=chatbot_response, is_bot=True)

        # redirect to chat page, so that the page is refreshed
        # and the new message is displayed
        return redirect('chat')


def login_view(request):
    '''Login page'''
    if request.user.is_authenticated:
        # user is already logged in, redirect to chat page
        return redirect('chat')

    if request.method == 'POST':
        # if request is post, authenticate user and log them in
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # authentication success, log the user in
                login(request, user)
                return redirect('chat')
        # authentication failed, back to login page
        return redirect('login')

    else:
        # if request is GET and user is not logged in, render login page
        return render(request, 'login.html')


def logout_view(request):
    '''Logs out user'''
    logout(request)
    global chatbot
    chatbot = Chatbot()  # reset chatbot
    return redirect('login')


def signup_view(request):
    '''Signup page'''

    # new signup request
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # create user form
        if form.is_valid():
            # save user to database
            user = form.save()
            login(request, user)
            return redirect('chat')  # signup success, redirect to chat page
        else:
            # signup failed, redirect to signup page
            return redirect('signup')
    else:
        # if request is GET, render signup page
        return render(request, 'signup.html')
