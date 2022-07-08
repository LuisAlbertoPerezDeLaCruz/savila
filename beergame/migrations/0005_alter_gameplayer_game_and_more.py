# Generated by Django 4.0.5 on 2022-07-05 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beergame', '0004_gameplayer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameplayer',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='beergame.game'),
        ),
        migrations.AlterUniqueTogether(
            name='gameplayer',
            unique_together={('game', 'player')},
        ),
    ]