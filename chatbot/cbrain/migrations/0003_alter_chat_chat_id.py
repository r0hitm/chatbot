# Generated by Django 4.1.7 on 2023-03-14 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbrain', '0002_rename_session_id_chat_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='chat_id',
            field=models.CharField(max_length=100),
        ),
    ]
