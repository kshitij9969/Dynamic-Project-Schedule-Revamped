# Generated by Django 3.0.8 on 2020-07-13 09:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200713_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=uuid.UUID('c445c371-4243-4e30-b227-700309d41c5f'), max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]
