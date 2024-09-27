# Generated by Django 5.1.1 on 2024-09-27 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MemberList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('first_name', models.CharField(max_length=255)),
                ('first_name_kana', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('last_name_kana', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('telephon_number', models.CharField(blank=True, max_length=15, null=True)),
                ('cellular_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('date_of_entry', models.DateField()),
                ('retire_age_month', models.CharField(blank=True, max_length=7, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_retire', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Meibo.city')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Meibo.department')),
            ],
        ),
    ]
