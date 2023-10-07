#!/usr/bin/python3
""" New db engine """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.base_model import Base
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.user import User


class DBStorage:
    """ class that creates engine and session that links to the database """
    __engine = None
    __sesssion = None

    def __init__(self):
        ''' Initializes the new storage engine'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format
                                      (getenv('HBNB_MYSQL_USER'),
                                       getenv('HBNB_MYSQL_PWD'),
                                       getenv('HBNB_MYSQL_HOST'),
                                       getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') is 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns objects depending on cls name """
        classes = [City, Review, State, City, Amenity, Place]
        objects = {}
        if cls is None:
            for item in classes:
                query = self.__session.query(item).all
                for obj in query:
                    obj_key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[obj_key] = obj
            return objects
        else:
            query = self.__session.query(cls).all
            for obj in query:
                obj_key = f"{obj.__class__.__name__}.{obj.id}"
                objects[obj_key] = obj
            return objects

    def new(self, obj):
        """ addsa new object to the current
        obejcts """
        self.__session.add(obj)

    def save(self):
        """ commits changes to the current
        database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes and object """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ creating the database engine """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        my_session = scoped_session(Session)
        self.__session = my_session()
