# Generated by Django 3.0.3 on 2020-02-20 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_connection_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
