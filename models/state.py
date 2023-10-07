#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import models


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', back_populates='state',
                          cascade='all, delete, delete-orphan')

    @property
    def cities(self):
        """ gettter method that returns
        all cities related to State """
        from models import storage
        s_instances = []
        cities = storage.all(City).values()

        for city in cities:
            if city.state_id == self.id:
                s_instances.append(city)
        return s_instances
