from django.shortcuts import render
from .models import Chat, Message
from .chatbot import Chatbot


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
