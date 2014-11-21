'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from cocktailor.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
#     restaurant_id = db.Column(db.Integer)

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self):
        """Saves a group"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Deletes a group"""
        db.session.delete(self)
        db.session.commit()
        return self
    
    def values(self):
        values = {}
        values['id'] = self.id
        values['name'] = self.name
        values['description'] = self.description
#         values['restaurant_id'] = self.restaurant_id
        return values
    
    def insert_name(self,name):
        self.name = name
        return self.name
    
    def insert_description(self,des):
        self.description = des
        return self.description
    

class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    price = db.Column(db.Integer)
    thumbnail = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    category_id = db.Column(db.Integer); 

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self):
        """Saves a group"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Deletes a group"""
        db.session.delete(self)
        db.session.commit()
        return self
    
    def values(self):
        values = {}
        values['id'] = self.id
        values['name'] = self.name
        values['description'] = self.description
        values['price'] = self.price
        values['thumbnail'] = self.thumbnail
        values['picture'] = self.picture
        values['category_id'] = self.category_id
        return values
    
    def insert_name(self,name):
        self.name = name
        return self.name
    
    def insert_description(self,des):
        self.description = des
        return self.description
    
    def insert_price(self,price):
        self.price = price
        return self.price
    
    def insert_category_id(self,c_id):
        self.category_id = c_id
        return self.category_id
    
