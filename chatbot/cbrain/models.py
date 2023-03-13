from django.contrib.auth.models import User
from django.db import models

"""
Models for the chatbot app (chatbot/cbrain/models.py)

The Chat model represents a chat session between a user and the chatbot.
Each chat session has a unique ID, a foreign key to the user that owns it,
and function to get the chat history.

The ChatHistory model represents a message sent by the user or the chatbot.
Each message has a unique ID, a foreign key to the chat session it belongs to,
the text of the message, timestamp, and isBot flag.
"""


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)

    def get_history(self):
        return ChatHistory.objects.filter(chat_session=self).order_by('timestamp')


class ChatHistory(models.Model):
    chat_session = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_bot = models.BooleanField(default=False)


class Chatbot(models.Model):
    name = models.CharField(max_length=100, default='Chatbot')
    # questions = models.ManyToManyField('Question')

    def respond(self, message):
        return 'I am a chatbot, and I do not respond to messages yet.'