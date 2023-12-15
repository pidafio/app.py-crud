from flask import Flask, render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://root:miletic5@localhost:3306/producto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria= db.Column(db.String(50))
    imagen = db.Column(db.String(600))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    descripcion=db.Column(db.String(500))
    precio = db.Column(db.Integer)
    def __init__(self, categoria, imagen, marca, modelo, descripcion, precio ) :
        self.categoria= categoria
        self.modelo= modelo
        self.imagen= imagen
        self.marca= marca
        self.descripcion= descripcion
        self.precio= precio
        


        
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return f'web para ingresar producto'

@app.route("/registro", methods=["POST"])
def registro():
    categoria_ingresada= request.json['categoria']
    img_ingresada= request.json['imagen']
    marca_ingresada= request.json['marca']
    modelo_ingresado= request.json['modelo']
    descripcion_ingresado=request.json['descripcion']
    precio_ingresado= request.json['precio']
    new_registro= Productos(categoria = categoria_ingresada, imagen = img_ingresada, marca= marca_ingresada, modelo=modelo_ingresado,descripcion=descripcion_ingresado, precio = precio_ingresado) 
    db.session.add(new_registro)
    db.session.commit()
    return "solicitud recibida"

@app.route('/productos', methods=['GET'])
def productos():
    total_registro=Productos.query.all()
    datos_serializada=[]
    for objeto in total_registro:
        datos_serializada.append({"id": objeto.id,"categoria":objeto.categoria, "imagen":objeto.imagen, "marca":objeto.marca, "modelo":objeto.modelo,"descripcion":objeto.descripcion, "precio": objeto.precio})
    return jsonify(datos_serializada)

@app.route('/upgrade/<id>', methods=['PUT'])
def upgrade(id):

    upgrade_producto=Productos.query.get(id)

    categoria_ingresada= request.json['categoria']
    img_ingresada= request.json['imagen']
    marca_ingresada= request.json['marca']
    modelo_ingresado= request.json['modelo']
    descripcion_ingresado=request.json['descripcion']
    precio_ingresado= request.json['precio']

    upgrade_producto.categoria=categoria_ingresada
    upgrade_producto.imagen=img_ingresada
    upgrade_producto.marca=marca_ingresada
    upgrade_producto.modelo= modelo_ingresado
    upgrade_producto.descripcion=descripcion_ingresado
    upgrade_producto.precio= precio_ingresado

    db.session.commit()

    datos_serializada=[{"id": upgrade_producto.id,"categoria": upgrade_producto.categoria, 'imagen':upgrade_producto.imagen, 'marca':upgrade_producto.marca, 'modelo':upgrade_producto.modelo, "descripcion":upgrade_producto.descripcion, 'precio': upgrade_producto.precio}]
    return jsonify(datos_serializada)

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    producto_delete=Productos.query.get(id)
    db.session.delete(producto_delete)
    db.session.commit()
    datos_serializada=({"id": producto_delete.id,'categoria':producto_delete.categoria, 'imagen':producto_delete.imagen, 'marca':producto_delete.marca, 'modelo':producto_delete.modelo, 'descripcion':producto_delete.descripcion, 'precio': producto_delete.precio})
    return jsonify(datos_serializada)

if __name__ == "__main__":
    app.run(debug=True)