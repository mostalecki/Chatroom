# Generated by Django 3.1.4 on 2021-04-01 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20210328_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='user_avatar_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]