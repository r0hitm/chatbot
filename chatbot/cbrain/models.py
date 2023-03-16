from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    '''
    The Chat model represents a chat session between a user and the chatbot.
    Each chat session has a unique ID, a foreign key to the user that owns it,
    and function to get the chat history.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=100)

    def get_history(self):
        return ChatHistory.objects.filter(chat_session=self).order_by('timestamp')


class ChatHistory(models.Model):
    '''
    The ChatHistory model represents a message sent by the user or the chatbot.
    Each message has a unique ID, a foreign key to the chat session it belongs to,
    the text of the message, timestamp, and isBot flag.
    '''
    chat_session = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_bot = models.BooleanField(default=False)
