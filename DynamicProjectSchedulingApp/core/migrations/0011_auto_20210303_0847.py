# Generated by Django 3.0.8 on 2021-03-03 08:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210303_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=uuid.UUID('ab90834f-c38b-47f2-bd34-74d6266bcf05'), max_length=100, unique=True),
        ),
    ]
