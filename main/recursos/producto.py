from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.modelos import ProductoModel, RatingModel

class Producto(Resource):
    def get(self,id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        return producto.to_json()
    
    def delete(self,id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        return {'message': 'El producto fue eliminado exitosamente'}, 204
        
    def put(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        if not producto:
            return {'message': 'El producto no fue encontrado'}, 404
        
        data = request.get_json()
        if 'title' in data:
            producto.titulo_prod = data['title']
        if 'price' in data:
            producto.precio_prod = data['price']
        if 'description' in data:
            producto.descripcion_prod = data['description']
        if 'category' in data:
            producto.categoria_prod = data['category']
        if 'image' in data:
            producto.imagen_url = data['image']

        rating_data = data.get('rating')
        if rating_data:
            if producto.rating:
                producto.rating.rate_rating = rating_data.get('rate_rating')
                producto.rating.count_rating = rating_data.get('count_rating')
            else:
                rating = RatingModel(
                    rate_rating=rating_data.get('rate_rating'),
                    count_rating=rating_data.get('count_rating')
                )
                producto.rating = rating
        db.session.commit()
        return producto.to_json(), 200

    

class Productos(Resource):
    def get(self):
        productos = db.session.query(ProductoModel)

        precio_min = request.args.get('precioMinimo')
        precio_max = request.args.get('precioMaximo')

        if precio_min:
            try:
                precio_min = float(precio_min)
                productos = productos.filter(ProductoModel.precio_prod >= precio_min)
            except ValueError:
                return {'message': 'El parámetro precioMinimo debe ser un número válido'}, 400

        if precio_max:
            try:
                precio_max = float(precio_max)
                productos = productos.filter(ProductoModel.precio_prod <= precio_max)
            except ValueError:
                return {'message': 'El parámetro precioMaximo debe ser un número válido'}, 400

        productos = productos.all()

        return jsonify([producto.to_json() for producto in productos])





    def post(self):
        data = request.get_json()
        product_data = {
            "titulo_prod": data.get('title'),
            "precio_prod": data.get('price'),
            "descripcion_prod": data.get('description'),
            "categoria_prod": data.get('category'),
            "imagen_url": data.get('image'),
        }
        producto = ProductoModel.from_json(product_data)
        rating_data = data.get('rating')
        if rating_data:
            rating = RatingModel(
                rate=rating_data.get('rate_rating'),
                count=rating_data.get('count_rating')
            )
            producto.rating = rating
            db.session.add(rating)
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201
    
