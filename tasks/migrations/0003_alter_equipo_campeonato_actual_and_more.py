# Generated by Django 5.1.2 on 2024-10-31 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_campeonato_cancha_statjugador_equipo_jugador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='campeonato_actual',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.campeonato'),
        ),
        migrations.AlterField(
            model_name='jugador',
            name='stat_jugador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.statjugador'),
        ),
    ]