# Generated by Django 3.0.8 on 2020-07-24 07:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=uuid.UUID('407cb699-f78d-4deb-994a-5196f89431a2'), max_length=100, unique=True),
        ),
    ]
