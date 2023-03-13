from django.contrib.auth.models import User
from django.db import models
# from django.utils.timezone import now


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

    expected_answers_list = property(
        get_expected_answers_list, set_expected_answers_list)
