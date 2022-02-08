from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.FLOAT(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel', back_populates='items')


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # create json method in order to return the item model in json format
    def json(self):
        return {'name': self.name, 'price': self.price}

    # A class method is a method that is bound to a class rather than its object.
    # It doesn't require creation of a class instance, much like staticmethod.
    @classmethod
    def find_by_name(cls, name):
        return ItemModel.query.filter_by(name=name).first() # == SELECT * FROM item WHERE name=name LIMIT1

    # sqlalchemy add item is good for inset and update so we will implement just one method
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
