# Generated by Django 4.1.7 on 2023-03-22 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_mail_is_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='subject',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]