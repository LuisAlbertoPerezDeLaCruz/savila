# Generated by Django 4.0.5 on 2022-07-24 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_bot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_bot',
            field=models.BooleanField(default=False, verbose_name='robot'),
        ),
    ]
