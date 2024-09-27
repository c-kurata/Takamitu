# Generated by Django 5.1.1 on 2024-09-27 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mitumori.department')),
            ],
        ),
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimate_name', models.CharField(max_length=255)),
                ('submit_to_name', models.CharField(max_length=255)),
                ('estimate_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('summary', models.TextField()),
                ('admin_approval_status', models.CharField(choices=[('', '選択してください'), ('承認', '承認'), ('未承認', '未承認')], max_length=50)),
                ('submission_date', models.DateField()),
                ('attachment', models.FileField(upload_to='attachments/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_estimates', to='Mitumori.employee')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mitumori.department')),
                ('last_updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_estimates', to='Mitumori.employee')),
            ],
        ),
    ]