'''
Created on 2014. 11. 29.

@author: hnamkoong
'''

from cocktailor.extensions import db

class FunctionalCallName(db.Model):
    __tablename__ = "functionalcallnames"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer)
    picture = db.Column(db.String(200))
    name = db.Column(db.Text)

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
        values['restaurant_id'] = self.restaurant_id
        values['picture'] = self.picture
        values['name'] = self.name
        return values
    
    def insert_name(self, n):
        self.name = n
        return self.name
    
    def insert_picture(self,p):
        self.picture = p
        return self.picture
    
    def insert_restaurant_id(self,rid):
        self.restaurant_id = rid
        return self.restaurant_id
    
class WaiterCall(db.Model):
    __tablename__ = "waitercalls"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer)
    device_id = db.Column(db.String(100))
    ble_id = db.Column(db.String(100))
    table = db.Column(db.String(100))
    functional_call_name = db.Column(db.String(100))
    waiter_name = db.Column(db.String(100)) 
    time = db.Column(db.String(100))

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
        values['device_id'] = self.device_id
        values['ble_id'] = self.ble_id
        values['table'] = self.table
        values['functional_call_name'] = self.functional_call_name
        values['time'] = self.time
        values['waiter_name'] = self.waiter_name
        return values
    
