from django.shortcuts import render,get_object_or_404
from .models import Categoria, Producto, Cliente

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

""" VISTAS PARA EL CARRITO DE COMPRAS"""

from .carrito import Cart
from django.shortcuts import redirect

def carrito(request):
    """Vista para mostrar el carrito de compras"""
    return render(request, 'carrito.html')

def agregarCarrito(request, producto_id):
    """Vista para agregar un producto al carrito de compras"""
    
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1

    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto, cantidad)

    #print(request.session.get('cart'))

    if request.method == 'GET':
        return redirect('/')
    return render(request, 'carrito.html')

def eliminarProductoCarrito(request, producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request, 'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request, 'carrito.html')

"""VISTAS PARA CLIENTES Y USUARIOS"""
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ClienteForm
from django.contrib.auth.decorators import login_required

def crearUsuario(request):
    """Vista para crear un nuevo usuario"""
    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario, password=dataPassword)
        if nuevoUsuario is not None:
            login(request, nuevoUsuario)
            return redirect('/cuenta/')
    return render(request, 'login.html')


def logoutUsuario(request):
    """Vista para cerrar sesión del usuario"""
    logout(request)
    return render(request,'login.html')


def cuentaUsuario(request):
    """Vista para mostrar la cuenta del usuario"""
    try:
        clienteEditar = Cliente.objects.get(user=request.user)

        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
            'direccion': clienteEditar.direccion,
            'telefono': clienteEditar.telefono,
            'dni': clienteEditar.dni,
            'sexo': clienteEditar.sexo,
            'fecha_nacimiento': clienteEditar.fecha_nacimiento,
        }
    except:
        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
        }
    
    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente': frmCliente,
    }
    return render(request, 'cuenta.html', context)


def loginUsuario(request):
    paginaDestino = request.GET.get('next',None)
    context = {
        'destino': paginaDestino,
    }

    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        usuarioAuth=authenticate(request, username=dataUsuario, password=dataPassword)
        if usuarioAuth is not None:
            login(request, usuarioAuth)
            if dataDestino != 'None':
                
                return redirect(dataDestino)
            return redirect('/cuenta')
        else:
            context= {
                'mensajeError': 'Usuario o contraseña incorrectos'
                }
    return render(request, 'login.html', context)



def actualizarCliente(request):
    """Vista para actualizar los datos del cliente"""
    mensaje = " "
    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data


            #actualizamos el usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente['nombre']
            actUsuario.last_name = dataCliente['apellidos']
            actUsuario.email = dataCliente['email']
            actUsuario.save()

            #registrar Cliente
            nuevoCliente = Cliente()
            nuevoCliente.user = actUsuario
            nuevoCliente.dni = dataCliente['dni']
            nuevoCliente.direccion = dataCliente['direccion']
            nuevoCliente.telefono = dataCliente['telefono']
            nuevoCliente.sexo = dataCliente['sexo']
            nuevoCliente.fecha_nacimiento = dataCliente['fecha_nacimiento']
            nuevoCliente.save()

            mensaje = "Datos actualizados correctamente"
    context = {
        'mensaje': mensaje,
        'frmCliente': frmCliente,
    }
    return render(request, 'cuenta.html', context)

""" VISTA PARA PROCESO DE COMPRA"""
@login_required(login_url='/login/')
def registrarPedido(request):
    """Vista para registrar un nuevo pedido"""
    try:
        clienteEditar = Cliente.objects.get(user=request.user)

        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
            'direccion': clienteEditar.direccion,
            'telefono': clienteEditar.telefono,
            'dni': clienteEditar.dni,
            'sexo': clienteEditar.sexo,
            'fecha_nacimiento': clienteEditar.fecha_nacimiento,
        }
    except:
        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
        }
        
    frmCLiente = ClienteForm()
    context = {
        'frmCliente': frmCLiente,
    }
    return render(request, 'pedido.html', context)