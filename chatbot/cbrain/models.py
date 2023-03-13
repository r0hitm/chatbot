from django.contrib.auth.models import User
from django.db import models

"""
Models for the chatbot app (chatbot/cbrain/models.py)

The Chat model represents a chat session between a user and the chatbot.
Each chat session has a unique ID, a foreign key to the user that owns it,
and a list of messages.

The Message model represents a message sent by the user or the chatbot.
Each message has a unique ID, a foreign key to the chat session it belongs to,
the text of the message, and the sender (either 'user' or 'bot').

The Question model represents a question that the chatbot can ask the user.
Each question has a unique ID, the text of the question, and a list of
possible answers. The list of answers is stored as a comma-separated list
in the database, but is exposed as a list of strings to the rest of the app.
"""

class Chat(models.Model):
    id = models.AutoField(primary_key=True)

    # Foreign key to the user (Django's User model) that owns this chat
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_chat_history(self):
        return Message.objects.filter(chat=self).order_by('created_at')


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='messages', default=None)
    text = models.TextField()
    sender = models.CharField(max_length=255, default='user')
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    # comma-separated list of answers
    expected_answers = models.CharField(max_length=255)

    def get_expected_answers_list(self):
        return self.expected_answers.split(',')

    def set_expected_answers_list(self, value):
        self.expected_answers = ','.join(value)

    # property to access the list of answers as a list
    expected_answers_list = property(
        get_expected_answers_list, set_expected_answers_list)
