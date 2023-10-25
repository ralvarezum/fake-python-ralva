from .. import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo_prod = db.Column(db.String(255),nullable=False)
    precio_prod = db.Column(db.Numeric(precision=10,scale=2),nullable=False)
    descripcion_prod = db.Column(db.String(255))
    categoria_prod = db.Column(db.String(255))
    imagen_url = db. Column(db.String(255))

    rating = db.relationship('Rating', uselist=False, back_populates='Producto', cascade='all, delete-orphan')

    def to_json(self):
        Producto_json = {
            'id': self.id,
            'titulo_prod': str(self.titulo_prod),
            'precio_prod': str(self.precio_prod),
            'descripcion_prod': str(self.descripcion_prod),
            'categoria_prod': str(self.categoria_prod),
            'imagen_url': str(self.imagen_url),

        }
        return Producto_json


    @staticmethod
    def from_json(Producto_json):
        id = Producto_json.get('id')
        titulo_prod = Producto_json.get('titulo_prod')
        precio_prod = Producto_json.get('precio_prod')
        descripcion_prod = Producto_json.get('descripcion_prod')
        categoria_prod = Producto_json.get('categoria_prod')
        imagen_url = Producto_json.get('imagen_url')
        return Producto(id=id,
                    titulo_prod=titulo_prod,
                    precio_prod=precio_prod,
                    descripcion_prod=descripcion_prod,
                    categoria_prod=categoria_prod,
                    imagen_url=imagen_url
                    )
    
    def __repr__(self):
        return '<Producto: %r %r %r %r %r>'% (self.titulo_prod, self.precio_prod, self.descripcion_prod, self.categoria_prod, self.imagen_url)