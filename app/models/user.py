from sqlalchemy import Column, Integer, String

from app.models.base import Base
from random import getrandbits
from app.util.hash import hash_pbkdf2

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    password = Column(String)
    coins = Column(Integer)
    salt = Column(String)

    def get_coins(self):
        return self.coins

    def credit_coins(self, i):
        self.coins += i

    def debit_coins(self, i):
        self.coins -= i

def create_user(db, username, password):
    random_salt = getrandbits(128).to_bytes(16, byteorder='little').hex()
    salted_password = hash_pbkdf2(password,random_salt)
    user = User(
        username=username,
        salted_password=salted_password,
        coins=100,
        salt = random_salt
    )
    db.add(user)
    return user

def get_user(db, username):
    return db.query(User).filter_by(username=username).first()


