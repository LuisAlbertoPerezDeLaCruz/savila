# Generated by Django 4.0.5 on 2022-07-10 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beergame', '0006_tokenforrefresh'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='max_turns',
            field=models.IntegerField(default=25),
        ),
        migrations.AlterField(
            model_name='gameplayer',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='beergame.game'),
        ),
        migrations.CreateModel(
            name='GameTurn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.IntegerField(default=0)),
                ('value_played', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('turn_result', models.CharField(max_length=500)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gameplayers', to='beergame.gameplayer')),
            ],
        ),
    ]
