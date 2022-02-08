from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # we dont want each time When create StoreModel to create each ItemModel that belong to him
    # so when use lazy, the self.item is now a query and to get all item -> self.item.all()
    items = db.relationship('ItemModel', lazy='dynamic',  back_populates='store')

    def __init__(self, name):
        self.name = name

    # create json method in order to return the item model in json format
    def json(self):
        return {'name': self.name,'id': self.id, 'items': [item.json() for item in self.items.all()]}

    # A class method is a method that is bound to a class rather than its object.
    # It doesn't require creation of a class instance, much like staticmethod.
    @classmethod
    def find_by_name(cls, name):
        return StoreModel.query.filter_by(name=name).first() # == SELECT * FROM item WHERE name=name LIMIT1

    # sqlalchemy add item is good for inset and update so we will implement just one method
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
