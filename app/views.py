# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages() #llama a la función que arma las cards.
    favourite_list = services.getAllFavourites(request) #esto llama a la lista de favoritos que esta en el services

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    
    name = request.POST.get('query', '').strip().lower() #el strip es para que elimine espacios al princio y al final de la cadena.


    if name == '': #si no escribió nada (cadena vacía), mostramos todas las imágenes
        images = services.getAllImages()
    else:
        all_images = services.getAllImages() # si escribió algo traemos todas las imágenes
        images = []
        for img in all_images: #se recorren todas las imágenes y nos quedamos con las que coinciden
            if name in img.name.lower(): #si el nombre escrito por el usuario está en en el nombre del pokemon.
                images.append(img) #se agrega a la lista
    if request.user.is_authenticated:  # si el usuario está logueado, traemos su lista de favoritos
        favourite_list = services.getAllFavourites(request)
    else: # si no lo está devuelve una lista vacía.
        favourite_list = []

        
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    
        

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    if request.method == 'POST':
        type_filter = request.POST.get('type')
        images = services.filterByType(type_filter)  # ← usamos "images" como en home()
        favourite_list = services.getAllFavourites(request)
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')
# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')