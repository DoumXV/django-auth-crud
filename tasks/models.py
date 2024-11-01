from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Task(models.Model):
    tittle = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tittle + '  -  ' + self.user.username


class Campeonato(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre


class Cancha(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=300)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=200)
    titulos = models.IntegerField()
    cancha_local = models.ForeignKey(Cancha,
                                     on_delete=models.CASCADE)
    campeonato_actual = models.ForeignKey(Campeonato,
                                          on_delete=models.CASCADE,
                                          null=True)

    def __str__(self):
        return self.nombre


class StatJugador(models.Model):
    p_jugados = models.IntegerField(default=0)
    t_amarrilas = models.IntegerField(default=0)
    t_rojas = models.IntegerField(default=0)
    goles = models.IntegerField(default=0)
    asistencias = models.IntegerField(default=0)

    def __str__(self):
        return str(self.p_jugados)


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=200)
    fecha_nacimiento = models.DateTimeField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    stat_jugador = models.OneToOneField(
        StatJugador, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre + ' - ' + self.equipo.nombre


# Señal para crear automáticamente StatJugador cuando se crea un Jugador
@receiver(post_save, sender=Jugador)
def create_stat_jugador(sender, instance, created, **kwargs):
    if created and instance.stat_jugador is None:
        stat = StatJugador.objects.create()
        instance.stat_jugador = stat
        instance.save()
