# Generated by Django 3.1.4 on 2021-04-22 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20210412_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='user_avatar_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
