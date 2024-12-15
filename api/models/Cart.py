from api import db


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


    def __str__(self):
        return '<Cart %r>' % self.id