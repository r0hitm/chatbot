from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from cbrain.models import Chat, Message


def home(request):
    return render(request, 'base.html')


def chat(request):
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

        # Create message object for user input
        message = Message.objects.create(
            chat=chat, text=user_message, sender='user')

        # Get chatbot response
        chatbot = Chatbot()
        chatbot_response = chatbot.respond(user_message)

        # Create message object for chatbot response
        message = Message.objects.create(
            chat=chat, text=chatbot_response, sender='chatbot')

        # Get chat history for this chat
        chat_history = Message.objects.filter(chat=chat).order_by('-timestamp')

        # Render chat template with chat history and new message
        return render(request, 'chat.html', {'chat_history': chat_history, 'new_message': chatbot_response})
    else:
        # Render empty chat template for initial page load
        return render(request, 'chat.html', {})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('chat')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
