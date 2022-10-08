from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Float,Date, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

class Usuario(UserMixin,db.Model):
    __tablename__='usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombreCompleto=Column(String,nullable=False)
    direccion=Column(String,nullable=False)
    telefono=Column(String,nullable=False)
    email=Column(String,unique=True)
    password=Column(String(128),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)
    genero=Column(String,nullable=False)

    def validarPassword(self,passw):
        if self.password == passw:
            return True
        else:
            return False

    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus=='Activo':
            return True
        else:
            return False
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False
    def is_vendedor(self):
        if self.tipo=='Vendedor':
            return True
        else:
            return False
    def is_comprador(self):
        if self.tipo=='Comprador':
            return True
        else:
            return False
    #Definir el método para la autenticacion
    def validar(self,email,password):
        usuario=Usuario.query.filter(Usuario.email==email).first()
        if usuario!=None and usuario.validarPassword(password) and usuario.is_active():
            return usuario
        else:
            return None
    #Método para agregar una cuenta de usuario
    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        u = self.consultaIndividual(id)
        db.session.delete(u)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Usuario.query.get(id)

class Producto(db.Model):
    __tablename__ = 'productos'
    id_producto = Column(Integer, primary_key = True)
    nombre = Column(String)
    descripcion = Column(String)
    precio = Column(Float)

    def consultaIndividual(self, id):
        return Producto.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        p = self.consultaIndividual(id)
        db.session.delete(p)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

class Carrito(db.Model):
    __tablename__='Carrito'
    idCarrito=Column(Integer,primary_key=True)
    idUsuario=Column(Integer,ForeignKey('usuarios.idUsuario'))
    id_Producto=Column(Integer,ForeignKey('productos.id_producto'))
    fecha=Column(Date,default=datetime.date.today())
    cantidad=Column(Integer,nullable=False,default=1)
    status=Column(String,nullable=False,default='Pendiente')
    producto=relationship('Producto',backref='carrito',lazy='select')
    usuario=relationship('Usuario',backref='carrito',lazy='select')

    def consultaIndividual(self, id):
        return Carrito.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        p = self.consultaIndividual(id)
        db.session.delete(p)
        db.session.commit()

    def consultaGeneral(self,idUsuario):
        return self.query.filter(Carrito.idUsuario==idUsuario).all()

class Tarjeta(db.Model):
    __tablename__ = 'tarjetas'
    idTarjeta = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuarios.idUsuario'))
    noTarjeta = Column(String, nullable=False)
    saldo = Column(Float, nullable=False)
    banco = Column(String, nullable=False)
    estatus = Column(String, nullable=False)

    def consultaIndividual(self, id):
        return Tarjeta.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        p = self.consultaIndividual(id)
        db.session.delete(p)
        db.session.commit()

    def consultaGeneral(self,idUsuario):
        return self.query.filter(Tarjeta.idUsuario==idUsuario).all()

class Pedido(db.Model):
    __tablename__ = 'Pedidos'
    idPedido = Column(Integer, primary_key=True, nullable=False)
    idComprador = Column(Integer, ForeignKey('usuarios.idUsuario'), nullable=False)
    idVendedor = Column(Integer, ForeignKey('usuarios.idUsuario'), nullable=False)
    idTarjeta = Column(String, ForeignKey('tarjetas.idTarjeta'),nullable=False)
    fechaRegistro = Column(String, nullable=False,default=datetime.date.today())
    fechaAtencion = Column(String, nullable=False,default=datetime.date.today())
    fechaRecepcion = Column(String, nullable=False,default=datetime.date.today())
    fechaCierre = Column(String, nullable=False,default=datetime.date.today())
    total = Column(Float, nullable=False)
    estatus = Column(String, nullable=False,default='Pendiente')

    def consultaIndividual(self, id):
        return Pedido.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        p = self.consultaIndividual(id)
        db.session.delete(p)
        db.session.commit()

    def consultaGeneral(self,idUsuario):
        return self.query.filter(Pedido.idComprador==idUsuario).all()

class DetallePedido(db.Model):
    __tablename__ = 'DetallePedidos'
    idDetalle= Column(Integer, primary_key=True, nullable=False)
    idPedido = Column(Integer, ForeignKey('Pedidos.idPedido'), nullable=False)
    idProducto = Column(Integer, ForeignKey('productos.id_producto'))
    precio = Column(Float)
    CANTIDADPEDIDA = Column(Integer, nullable=False, default=1)
    subTotal = Column(Float)
    estatus = Column(String, nullable=False,default='Activo')
    comentario = Column(String, nullable=False)
    producto = relationship('Producto', backref='detallePedido', lazy='select')
    pedido = relationship('Pedido', backref='detallePedido', lazy='select')

    def consultaIndividual(self, id):
        return DetallePedido.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        p = self.consultaIndividual(id)
        db.session.delete(p)
        db.session.commit()

    def consultaGeneral(self,idPedido):
        return self.query.filter(Pedido.idPedido==idPedido).all()
