# Generated by Django 4.1.7 on 2023-03-24 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_log_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='read_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='sent_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='mail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]