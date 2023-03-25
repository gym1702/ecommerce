
from applications.categorias.models import Categoria


def menu_links(request):
    links = Categoria.objects.all()

    #regresa un diccionario
    return dict(links = links)