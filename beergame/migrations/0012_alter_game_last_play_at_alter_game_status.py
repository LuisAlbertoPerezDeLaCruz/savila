# Generated by Django 4.0.5 on 2022-07-14 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beergame', '0011_alter_game_last_play_by_alter_game_next_play_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='last_play_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('C', 'Created'), ('S', 'Started'), ('A', 'Active'), ('I', 'Inactive'), ('C', 'Completed'), ('X', 'Expired')], default='C', max_length=1, verbose_name='Status'),
        ),
    ]
