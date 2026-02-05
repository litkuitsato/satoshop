from django.shortcuts import render,get_object_or_404
from .models import Categoria, Producto

# Create your views here.
""" VISTA PARA EL CATALOGO DE PRODUCTOS"""

def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    #print(listaProductos)
    context = {
        'productos': listaProductos,
        'categorias': listaCategorias,
    }
    return render(request, 'index.html', context)

def productosPorCategoria(request, categoria_id):
    """Vista para mostrar productos por categoria"""
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all()

    listaCategorias = Categoria.objects.all()
    context = {
        'productos': listaProductos,
        'categorias': listaCategorias,
    }
    return render(request, 'index.html', context)

def productosPorNombre(request):
    """Vista para filtrar productos por nombre"""
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__icontains=nombre)
    listaCategorias = Categoria.objects.all()
    context = {
        'productos': listaProductos,
        'categorias': listaCategorias,
    }
    return render(request, 'index.html', context)

def productoDetalle(request, producto_id):
    """Vista para mostrar el detalle de un producto"""
    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto, pk=producto_id)
    context = {
        'producto': objProducto,
    }
    return render(request, 'producto.html', context)