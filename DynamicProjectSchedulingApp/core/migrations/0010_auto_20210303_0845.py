# Generated by Django 3.0.8 on 2021-03-03 08:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210303_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=uuid.UUID('f35fd017-bce0-4903-8e27-23de868d9b82'), max_length=100, unique=True),
        ),
    ]