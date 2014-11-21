'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from cocktailor.extensions import db



class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_content = db.Column(db.Text)
    price = db.Column(db.Integer)
    table = db.Column(db.Integer)
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
        values['user_id'] = self.user_id
        values['order_content'] = self.order_content
        values['price'] = self.price
        values['table'] = self.table
        values['status'] = self.status
        return values
    
    def change_status(self):
        if self.status == 'pending':
            self.status = 'done'
        return
