__author__ = 'Ian S. Evans'

from collection_json import Collection, Template
from flask_crudsdb import Database
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, BigInteger, Binary, Boolean, Column, Constraint, Date, DateTime, Enum, Float, \
    ForeignKey, ForeignKeyConstraint, Index, Integer, Interval, LargeBinary, Numeric, PrimaryKeyConstraint, Sequence, \
    String, Table, Text, Time, Unicode, UnicodeText, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: Convert this to pure sqlalchemy

SQLAlchemyModel = declarative_base()


class SQLAlchemyDatabase(Database):
    """
    SQL flask_crudsdb wrapper
    """

    def __init__(self, app):
        super(Database, self).__init__(app)
        self.database = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))

    def create(self, model, data, **kwargs):
        """
        Create a new instance of a model
        :param model: The model name to create an instance of
        :type model: str
        :param data: The data to provide to that instance, formatted as a Collection+JSON data array
        :type data: list
        :return: Collection representation of the created resource.
        """
        try:
            data = Template(data)
        except (TypeError, ValueError, IndexError):
            abort(400)
        # letting this raise a KeyError on purpose, flask returns HTTP 500 on python errors
        instance = self.models[model](data)
        session = sessionmaker(bind=self.database)
        session.add(instance)
        session.commit()
        return Collection(href=self.app.config.get('API_ROOT'), items=[instance.get_collection_item()])

    def read(self, model, pk=None, **kwargs):
        """
        Read the database for a model instance by id.
        :param model: The model name to look for instances of.
        :type model: str
        :param pk: The primary key of the model instance to attempt to read.
        :param kwargs:
        :return: Collection representation of resource(s) retrieved from the database.
        """
        # letting self.models[model] raise a KeyError on purpose, see above
        response = Collection(
            href=self.app.config.get('API_ROOT'), template=self.models[model].get_collection_template()
        )
        session = sessionmaker(bind=self.database)
        if pk is None:
            instances = session.query(self.models[model])
            if kwargs.get('order_by'):
                instances = instances.order_by(getattr(self.models[model], kwargs['order_by']))
        else:
            instances = session.query(self.models[model]).get(pk)
            if instances is None:
                abort(404)
        for instance in instances:
            response.items.append(instance.get_collection_item())
        return response

    def update(self, model, data, pk=None, **kwargs):
        """
        Update a model instance in the database.
        :param model: The model name to look for an instance of.
        :param data: The data to provide to the instance, formatted as a Collection+JSON data array
        :param pk: The primary key of the model instance to modify.
        :param kwargs:
        :return: A Collection+JSON representation of the updated model instance.
        """
        try:
            data = Template(data)
        except (TypeError, ValueError, IndexError):
            abort(400)

        # letting self.models[model] raise a KeyError on purpose, see above
        instance = self.models[model].query.get_or_404(pk)
        instance.update(data)
        self.database.session.commit()
        return Collection(
            href=self.app.config.get('API_ROOT'), template=self.models[model].get_collection_template(),
            items=[instance.get_collection_item()]
        )

    def delete(self, model, pk=None, **kwargs):
        """
        Delete a model instance from the database by id.
        :param model: The name of the model to delete an instance of.
        :param pk: The primary key of the instance to delete.
        :param kwargs:
        :return:
        """
        # letting self.models[model] raise a KeyError on purpose, see above
        instance = self.models[model].query.get_or_404(pk)
        self.database.session.delete(instance)
        self.database.session.commit()

    def search(self, model, data, **kwargs):
        pass