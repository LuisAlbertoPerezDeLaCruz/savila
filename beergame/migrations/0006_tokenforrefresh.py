# Generated by Django 4.0.5 on 2022-07-07 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beergame', '0005_alter_gameplayer_game_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenForRefresh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=30)),
            ],
        ),
    ]
