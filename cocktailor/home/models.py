'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from cocktailor.extensions import db



class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer)
    order_content = db.Column(db.Text)
    price = db.Column(db.Integer)
    table = db.Column(db.Integer)
    time = db.Column(db.String(20))
    done_time=db.Column(db.String(20))
    status = db.Column(db.String(20))

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
        values['order_content'] = self.order_content
        values['price'] = self.price
        values['table'] = self.table
        values['time'] = self.time
        values['done_time'] = self.done_time
        values['status'] = self.status
        return values
    
    def insert_content(self,con):
        self.order_content = con
        return self.order_content
    
    def insert_price(self,pr):
        self.price = pr
        return self.price
    
    def insert_table(self,tb):
        self.table = tb
        return self.table
    
    def insert_time(self,time):
        self.time = time
        return self.time
    
    def insert_restaurant_id(self,restaurant_id):
        self.restaurant_id = restaurant_id
        return self.restaurant_id
    
    def insert_status(self):
        self.status = 'pending'
        return self.status
    
    def change_status(self, t):
        if self.status == 'pending':
            self.status = 'done'
            self.done_time = t
        return
