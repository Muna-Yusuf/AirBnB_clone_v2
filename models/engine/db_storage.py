#!/usr/bin/python3
""" new class for sqlAlchemy """
import os
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        hb_user = os.getenv("HBNB_MYSQL_USER")
        hb_pwd = os.getenv("HBNB_MYSQL_PWD")
        hb_host = os.getenv("HBNB_MYSQL_HOST")
        hb_db = os.getenv("HBNB_MYSQL_DB")
        hb_env = os.getenv("HBNB_ENV")


        engine = create_engine(
            f"mysql+mysqldb://{hb_user}:{hb_pwd}@{hb_host}/{hb_db}",
            pool_pre_ping=True)

        self.__engine = engine
        if hb_env == "test":
            Base.metadata.drop_all(engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        obj_list = [User, Place, State, City, Amenity, Review]
        objects = []

        if cls is not None:
            objects.extend(self.__session.query(cls).all())
        else:
            for items in obj_list:
                objects.extend(self.__session.query(items).all())
        dic = {}
        for obj in objects:
            k = f"{obj.__class__.__name__}.{obj.id}"
            dic[k] = obj
        return dic

    def new(self, obj):
        """add a new element in the table
        """
        self.__session.add(obj)

    def save(self):
        """save changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete an element in the table
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """configuration
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=(self.__engine), expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()
