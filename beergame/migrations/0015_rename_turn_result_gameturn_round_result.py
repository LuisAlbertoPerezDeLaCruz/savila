# Generated by Django 4.0.5 on 2022-07-14 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beergame', '0014_gameturn_round'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameturn',
            old_name='turn_result',
            new_name='round_result',
        ),
    ]
