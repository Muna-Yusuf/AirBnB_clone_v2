#!/usr/bin/python3
"""Module for SQLAlchemy database storage"""
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Database storage engine using SQLAlchemy"""

    __engine = None
    __session = None

    def init(self):
        """Initialize DBStorage instance"""
        hb_user = os.getenv("HBNB_MYSQL_USER")
        hb_pwd = os.getenv("HBNB_MYSQL_PWD")
        hb_host = os.getenv("HBNB_MYSQL_HOST")
        hb_db = os.getenv("HBNB_MYSQL_DB")
        hb_env = os.getenv("HBNB_ENV")

        # Create MySQL connection string
        connection_str = f"mysql+mysqldb://{hb_user}:{hb_pwd}@{hb_host}/{hb_db}"

        # Create SQLAlchemy engine
        engine = create_engine(connection_str, pool_pre_ping=True)

        self.__engine = engine
        if hb_env == "test":
            Base.metadata.drop_all(engine)

    def all(self, cls=None):
        """Query objects from the database"""
        classes = [State, City, User, Place, Review, Amenity]
        result = {}

        if cls:
            query = self.__session.query(cls).all()
        else:
            query = []
            for clazz in classes:
                query.extend(self.__session.query(clazz).all())

        for obj in query:
            key = "{}.{}".format(type(obj).name, obj.id)
            result[key] = obj
        return result

    def new(self, obj):
        """Add object to current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
