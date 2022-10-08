from flask import Flask,render_template,request
from modelo.Dao import db,Usuario,Producto, Carrito,Tarjeta, Pedido, DetallePedido
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import  session,redirect, url_for
from datetime import timedelta
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/tiendaMSC'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#gestion de usuarios
app.secret_key='Cl4v3'
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='index'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"


@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

# Urls definidas para el control de usuario
@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('index'))


#vistas de las diferentes rutas
@app.route('/')
def index():
     #return "hola mundo "+ str(x)
     if not current_user.is_authenticated:
         return render_template('login.html')
     return render_template('menu.html')

@app.route('/validarLogin', methods=['post'])
def validarLogin():
    nombre=request.form['nombre']
    p=request.form['pass']
    # usuarios=['antonio','juan','pedro']
    # contras=['123','456','789']
    # cont=0
    # for usuario in usuarios:
    #      if nombre == usuario and p==contras[cont]:
    #          return render_template('menu.html',usuario=usuario)
    #      cont=cont+1
    # return render_template('login.html',mensaje='usuario no valido')
    u=Usuario()
    u=u.validar(nombre, p)
    if u != None:
        login_user(u)
        return render_template('menu.html')
    return render_template('login.html',mensaje='usuario no valido')
        

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)


@app.route('/menu')
@login_required
def menuGral():
    return render_template('menu.html')

@app.route('/clientes')
def menuClientes():
    datos=[
           ['1001', 'juan','1000'],
           ['1002', 'pedro','2000'],
           ['1003', 'luis','3000']
           ]
    if current_user.is_authenticated and  current_user.is_admin():
        return render_template('clientes.html',datos=datos)
    return render_template('menu.html')

@app.route('/agregarcliente')
def clienteNuevo():
    if current_user.is_authenticated and  current_user.is_admin():
        return render_template('cliente_nuevo.html')
    return render_template('menu.html')


@app.route('/productos')
@login_required
def prooductos():
    prod= Producto()
    prods=prod.consultaGeneral()
    return render_template('productos.html',productos=prods)

@app.route('/agregarProducto')
@login_required
def productoNuevo():
    if current_user.is_authenticated and  current_user.is_admin():
        return render_template('producto_nuevo.html')
    return redirect(url_for('prooductos'))

@app.route('/guardarproducto', methods=['post','get'])
@login_required
def guardarProducto():
    id_producto=request.form['id_producto']
    nombre=request.form['nombre']
    descripcion=request.form['descripcion']
    precio=request.form['precio']
    prod = Producto()
    prod.id_producto=id_producto
    prod.nombre=nombre
    prod.descripcion=descripcion
    prod.precio=precio
    prod.agregar()
    prods=prod.consultaGeneral()
    return render_template('productos.html',productos=prods)

@app.route('/actualizarProducto/<id>')
@login_required
def actualizarProd(id):
    if current_user.is_authenticated and  current_user.is_admin():
        prod = Producto()
        prod = prod.consultaIndividual(id)
        return render_template('modificarProducto.html', producto=prod)
    return redirect(url_for('prooductos'))


@app.route('/modificarProducto',methods=['post'])
@login_required
def modificarProd():
    numProd = request.form['claveP']
    nombreP = request.form['nombreP']
    desP = request.form['descP']
    precioP = request.form['precioP']
    prod = Producto()
    prod.id_producto = numProd
    prod.nombre = nombreP
    prod.descripcion = desP
    prod.precio = precioP
    if current_user.is_authenticated and current_user.is_admin():
        prod.editar()
    prods = prod.consultaGeneral()
    return render_template('productos.html',productos=prods)

@app.route('/eliminarProd/<id>')
@login_required
def eliminarProd(id):
    prod = Producto()
    if current_user.is_authenticated and current_user.is_admin():
        prod.eliminar(id)
    prods = prod.consultaGeneral()
    return render_template('productos.html',productos=prods)

@app.route('/carrito')
@login_required
def carrito():
    cesta= Carrito()
    prods=cesta.consultaGeneral(current_user.idUsuario)
    return render_template('consultarCarrito.html',cesta=prods)

@app.route('/agregarCarrito/<id>')
@login_required
def agregarCarrito(id):
    prod = Producto()
    prod=prod.consultaIndividual(id)
    return render_template('agregarCarrito.html',producto=prod)

@app.route('/agregarProdCarrito',methods=['post'])
@login_required
def agregarProdCarrito():
    numProd = request.form['claveP']
    cantidad = request.form['cantidad']
    print(numProd)
    carrito = Carrito()
    carrito.id_Producto = numProd
    carrito.idUsuario = current_user.idUsuario
    carrito.cantidad = cantidad
    carrito.agregar()
    prod = Producto()
    prods = prod.consultaGeneral()
    return render_template('productos.html',  productos=prods)

@app.route('/eliminarProductoCarr/<id>')
@login_required
def eliminarProductoCarrito(id):
    carr = Carrito()
    carr.eliminar(id)
    carr = Carrito()
    prods = carr.consultaGeneral(current_user.idUsuario)
    return render_template('consultarCarrito.html', cesta=prods)

@app.route('/actualizarProductoCarrito/<id>')
@login_required
def actualizarProductoCarrito(id):
    carr=Carrito()
    carr=carr.consultaIndividual(id)
    return render_template('actualizarCarrito.html',carrito=carr)

@app.route('/modificarProductoCarrito',methods=['post'])
@login_required
def modificarProductoCarrito():
    id= request.form['idCarrito']
    cantidad = request.form['cantidad']
    carr = Carrito()
    carr = carr.consultaIndividual(id)
    carr.cantidad = cantidad
    carr.editar()
    prods = carr.consultaGeneral(current_user.idUsuario)
    return render_template('consultarCarrito.html', cesta=prods)

@app.route('/pedidos')
@login_required
def consultarPedidos():
    pedido= Pedido()
    pedidos=pedido.consultaGeneral(current_user.idUsuario)
    return render_template('mostrarPedidos.html',pedidos=pedidos)

@app.route('/mostrarPedido',methods=['post'])
@login_required
def mostrarPedido():
    ids = request.values.getlist('idCarrito')
    print (ids)
    tars= Tarjeta()
    tars=tars.consultaGeneral(current_user.idUsuario)
    #for t in tars:
    #    print(t)
    total=0
    for c in ids:
        carr=Carrito()
        carr=carr.consultaIndividual(c)
        subtotal=carr.producto.precio *carr.cantidad
        total=total +subtotal
    #print(total)
    return render_template('consultarPedido.html',  ids=ids,total=total,tarjetas=tars)
    #return 'Productos confirmados'

@app.route('/guardarPedido',methods=['post'])
@login_required
def guardarPedido():
    ids = request.values.getlist('ids')
    print(ids)
    total=request.values.getlist('total')
    t=request.form['idTarjeta']
    tar= Tarjeta()
    tar=tar.consultaIndividual(int(t))
    #print(tar)
    #print(t)
    pedido=Pedido()
    pedido.idComprador=current_user.idUsuario
    vendedor= Usuario()
    vendedor.idUsuario=1
    pedido.idVendedor= vendedor.idUsuario
    pedido.idTarjeta=tar.idTarjeta
    pedido.total=total
    pedido.agregar()
    for c in ids:
        print(c)
        carr=Carrito()
        carr=carr.consultaIndividual(int(c))
        print(carr)
        det = DetallePedido()
        det.idPedido = pedido.idPedido
        prod=Producto()
        prod=prod.consultaIndividual(carr.id_Producto)
        det.precio= prod.precio
        det.idProducto=prod.id_producto
        det.CANTIDADPEDIDA=carr.cantidad

        det.subTotal=det.precio*det.CANTIDADPEDIDA
        det.agregar()
        carr.eliminar(carr.idCarrito)
    carr = Carrito()
    prods = carr.consultaGeneral(current_user.idUsuario)
    return render_template('consultarCarrito.html', cesta=prods)



if __name__== '__main__':
    db.init_app(app)  # Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug= True)
    #app.run(debug=True,host='0.0.0.0',port=5000)

    