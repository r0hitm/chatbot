from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.decorators import login_required
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


# @login_required
def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Get user input
        user_message = request.POST.get('user_message')

        # Get chat object or create new one
        # chat_id = request.session.get('chat_id')
        chat = Chat.objects.filter(user=request.user).first()
        if not chat:
            chat = Chat.objects.create(user=request.user)
            # request.session['chat_id'] = chat.chat_id

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
        # chat_history = ChatHistory.objects.filter(chat_session=chat).order_by('-timestamp')
        chat_history = chat.get_history()

        # Render chat template with chat history and new message
        return render(request, 'chat.html', {'chat_history': chat_history})
        # return render(request, 'chat.html', {'new_message': chatbot_response, 'user_message': user_message})
    else:
        chat = Chat.objects.filter(user=request.user).first()
        # chat_id = request.session.get('chat_id')
        if chat:
            # chat = Chat.objects.get(chat_id=chat_id)
            chat_history = chat.get_history()
            return render(request, 'chat.html', {'chat_history': chat_history})
        else:
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
