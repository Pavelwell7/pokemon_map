import folium

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = timezone.localtime()
    active_entities = PokemonEntity.objects.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now,
    )
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in active_entities:
        pokemon = entity.pokemon
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            img_url,
        )
    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    now = timezone.localtime()
    active_requested_entities = PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        appeared_at__lte=now,
        disappeared_at__gte=now,
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in active_requested_entities:
        pokemon = entity.pokemon
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            img_url,
        )
    previous_evolution = requested_pokemon.previous_evolution
    next_evolution = requested_pokemon.next_evolutions.first()
    img_url = request.build_absolute_uri(requested_pokemon.photo.url) if requested_pokemon.photo else DEFAULT_IMAGE_URL
    pokemon_datails = {
        'pokemon_id': requested_pokemon.id,
        'img_url': img_url,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.text,
    }
    if previous_evolution:
        pokemon_datails['previous_evolution'] = {
            'title_ru': previous_evolution.title,
            'pokemon_id': previous_evolution.id,
            'img_url': request.build_absolute_uri(previous_evolution.photo.url) if previous_evolution.photo else DEFAULT_IMAGE_URL,
        }
    if next_evolution:
        pokemon_datails['next_evolution'] = {
            'title_ru': next_evolution.title
            ,
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.photo.url) if next_evolution.photo else DEFAULT_IMAGE_URL,
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_datails
    })
