from django.db import models  # noqa F401

class Pokemon(models.Model):

    title = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(null=True, blank=True, verbose_name='Описание')
    title_en = models.TextField(max_length=200, verbose_name='Название нп англ.')
    title_jp = models.TextField(max_length=200, verbose_name='Название на японском')
    previous_evolution = models.ForeignKey(
                                           'self',
                                           verbose_name='Из кого эволюционирует',
                                           null=True,
                                           blank=True,
                                           related_name='next_evolutions',
                                           on_delete=models.SET_NULL
    )
    photo = models.ImageField(upload_to='pokemon_photos/', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(null=True, blank=True, verbose_name='Широта')
    lon = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Появиться в')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Исчезнет в')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon.title} {self.level} lv'

