from django.shortcuts import render, redirect
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


def chat_view(request):
    # TODO: I don't know if this works
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Get user input
        user_message = request.POST.get('user_message')

        # Get chat object or create new one
        chat_id = request.session.get('chat_id')
        if chat_id:
            chat = Chat.objects.filter(chat_id=chat_id).first()
        else:
            chat = Chat.objects.create()
            request.session['chat_id'] = chat.chat_id

        # Save user message in the chat history
        chat_history = ChatHistory.objects.create(
            chat_session=chat, message=user_message, is_bot=False)

        # Get chatbot response
        chatbot = Chatbot()
        chatbot_response = chatbot.respond(user_message)

        # Save chatbot response in the chat history
        chat_history = ChatHistory.objects.create(
            chat_session=chat, message=chatbot_response, is_bot=True)

        # Get chat history for this chat
        chat_history = Message.objects.filter(chat=chat).order_by('-timestamp')

        # Render chat template with chat history and new message
        return render(request, 'chat.html', {'chat_history': chat_history, 'new_message': chatbot_response})
    else:
        # Render empty chat template for initial page load
        return render(request, 'chat.html', {})


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
        else:
            messages.error(request, 'Invalid username or password')
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
