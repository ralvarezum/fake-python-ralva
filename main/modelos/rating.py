from .. import db

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate_rating = db.Column(db.Numeric(precision=10,scale=2),nullable=False)
    count_rating = db.Column(db.Integer)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Producto', back_populates='rating')
    

    def to_json(self):
        rating_json = {
            'id': self.id,
            'rate_rating': str(self.rate_rating),
            'count_rating': str(self.count_rating),
        }
        return rating_json


    @staticmethod
    def from_json(rating_json):
        id = rating_json.get('id')
        rate_rating = rating_json.get('rate_rating')
        count_rating = rating_json.get('contador')
        return Rating(id=id,
                    rate_rating=rate_rating,
                    count_rating=count_rating,
                    )
    
    def __repr__(self):
        return '<Producto: %r %r %r>'% (self.rate_rating, self.count_rating)