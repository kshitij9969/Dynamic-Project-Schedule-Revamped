# Generated by Django 3.0.8 on 2020-07-23 15:46

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('profile_picture', models.ImageField(blank=True, default='', null=True, upload_to=core.models.rename_profile_picture)),
                ('username', models.CharField(default=uuid.UUID('5f9106ce-a86f-42ff-a74a-bda2080514ac'), max_length=100, unique=True)),
                ('email', models.EmailField(max_length=200)),
                ('full_name', models.CharField(max_length=100)),
                ('nick_name', models.CharField(max_length=50, null=True)),
                ('creation_date', models.DateField(auto_now_add=True, null=True)),
                ('account_update_date', models.DateField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='OrganisationAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry', models.CharField(max_length=50)),
                ('country_code', models.CharField(max_length=10)),
                ('contact_no', models.CharField(max_length=30)),
                ('address_line_one', models.CharField(max_length=30)),
                ('address_line_two', models.CharField(blank=True, max_length=30, null=True)),
                ('address_line_three', models.CharField(blank=True, max_length=40, null=True)),
                ('country', models.CharField(max_length=50)),
                ('province_state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=30)),
                ('account_verified', models.BooleanField(default=True)),
                ('user_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=10, unique=True)),
                ('belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.OrganisationAccount')),
                ('user_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssociateAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=10, unique=True)),
                ('belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.OrganisationAccount')),
                ('reports_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.ManagerAccount')),
                ('user_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
