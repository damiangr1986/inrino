# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    pokemon_lista=transport.getAllImages() #pedimos la lista de los pokemon con la info "desornedana, y lo guardamos en la variable pokemon_lista"
    cards=[] #inicamos una lista de tarjetas

    for poke_data in pokemon_lista: #recorremos cada pokemon de la lista
        card = translator.fromRequestIntoCard(poke_data) # a los datos de cada pokemon lo transformamos en tarjetas y le asignamos la variable card

        alt_names = poke_data.get('alternate_names', []) #obtenemos la lista de nombres alternativos o lista vacia si no hay
        if alt_names: #si hay nombres
            card.display_name = random.choice(alt_names) #elige uno al azar y se asigna como display_name
        else: 
            card.display_name = "No hay nombres alternativos para " + card.name #si no hay, muestra un mensaje con su nombre real

        cards.append(card) #agregamos una tarjeta a la lista nueva 
    return cards #devuelve la lista final de cards con toda la información

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)