# Generated by Django 3.0.8 on 2021-03-03 08:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210303_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=uuid.UUID('582be36d-60aa-4d5b-936f-8f91cd10080a'), max_length=100, unique=True),
        ),
    ]
