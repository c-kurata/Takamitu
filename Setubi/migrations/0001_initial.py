# Generated by Django 5.1.1 on 2024-09-27 16:38

import Setubi.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(default=Setubi.models.generate_random_color, max_length=7, verbose_name='色')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='氏名')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.CharField(max_length=100, verbose_name='現場名または施設名')),
                ('start_time', models.DateTimeField(verbose_name='開始日時')),
                ('end_time', models.DateTimeField(verbose_name='終了日時')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Setubi.equipment', verbose_name='設備')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Setubi.reservationuser', verbose_name='予約者')),
            ],
        ),
    ]
