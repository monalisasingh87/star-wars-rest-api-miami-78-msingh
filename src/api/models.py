from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


# many-to-many relationship between User and Person
User_Person_Favorites = Table('user_person_favorites',
      db.metadata,
      Column('user_id', ForeignKey('user.id'), primary_key=True, nullable=False),
      Column('person_id', ForeignKey('person.id'), primary_key=True, nullable=False),
        )

User_Planet_Favorites = Table('user_planet_favorites',
      db.metadata,
      Column('user_id', ForeignKey('user.id'), primary_key=True, nullable=False),
      Column('planet_id',ForeignKey('planet.id'), primary_key=True, nullable=False),
     )

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return'<User %r>' % self.username
    
    #relationship
    favorite_people: Mapped[list['Person']]= relationship(secondary= User_Person_Favorites, back_populates= 'favorited_by_user')
    favorite_planet: Mapped[list['Planet']]= relationship(secondary= User_Planet_Favorites, back_populates= 'favorited_by_user')
  
    def __repr__(self):
      return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }


class Person(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=True)
    
    #realtionship
    favorited_by_user: Mapped[list['User']] = relationship(secondary=User_Person_Favorites, back_populates= 'favorite_people')

    def __repr__(self):
        return'<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
        }
    
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=True)

        
    #realtionship
    favorited_by_user: Mapped[list['User']] = relationship(secondary=User_Planet_Favorites, back_populates= 'favorite_planet')


    def __repr__(self):
        return'<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
        }
    