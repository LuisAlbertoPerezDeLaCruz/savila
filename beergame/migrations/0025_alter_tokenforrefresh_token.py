# Generated by Django 4.0.5 on 2022-07-30 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beergame', '0024_rename_result_game_final_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenforrefresh',
            name='token',
            field=models.CharField(max_length=255),
        ),
    ]
