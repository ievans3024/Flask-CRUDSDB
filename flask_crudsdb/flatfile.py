__author__ = 'Ian S. Evans'

import json
from collection_json import Collection, Template
from collections import UserDict
from flask_crudsdb import Database
from flask import abort


class FlatDatabase(Database):
    """A flatfile database that operates in memory and stores on disk as json in user-configurable file"""
    class AutoKeyDict(UserDict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __setitem__(self, key, value):
            if key == 'next':
                key = len(sorted(self.data))
            elif type(key) != int:
                try:
                    key = int(abs(key))
                except (ValueError, TypeError):
                    raise TypeError('key must be parseable to an integer or "next"')
            super().__setitem__(key, value)

        def extend(self, d):
            super().__init__(dict(self.data), **d)

    class ModelJSONEncoder(json.JSONEncoder):
        def default(self, o, models={}):
            if o.__class__.__name__ in models:
                d = o.get_collection_item.to_dict()
                d['__class__'] = o.__class__.__name__
                return d
            elif isinstance(o, FlatDatabase.AutoKeyDict):
                d = o.data
                d['__class__'] = o.__class__.__name__
                return d
            else:
                return json.JSONEncoder.default(self, o)

    class ModelJSONDecoder(json.JSONDecoder):
        def decode(self, s, models={}, **kwargs):
            default = super().decode(s, **kwargs)
            if '__class__' in default:
                if default['__class__'] in models:
                    default = models[default['__class__']](**default)
                if default['__class__'] == 'AutoKeyDict':
                    default = FlatDatabase.AutoKeyDict(default)
            return default

    def __init__(self, app):
        super(FlatDatabase, self).__init__(app)
        self.database = {}
        try:
            self.__reload_db_file()
        except FileNotFoundError:
            self.__write_db_file()

    def __reload_db_file(self):
        with open(self.app.config.get('FLAT_DATABASE_FILE')) as db_file:
            self.database = json.load(db_file, cls=FlatDatabase.ModelJSONDecoder, models=self.models)

    def __write_db_file(self):
        with open(self.app.config.get('FLAT_DATABASE_FILE'), 'w') as db_file:
            json.dump(self.database, db_file, cls=self.ModelJSONEncoder, models=self.models)

    def create(self, model, data, *args, **kwargs):
        response = Collection(href=self.app.config.get('API_ROOT'))
        try:
            data = Template(data)
        except (TypeError, ValueError, IndexError):
            abort(400)
        instance = self.models[model](data)
        if (self.models.get(model)) and (not self.database.get(model)):
            self.database[model] = self.AutoKeyDict()
        self.database[model]['next'] = instance
        self.__write_db_file()  # TODO: Thread/Multiprocess this
        response.items.append(instance.get_collection_item())
        return response

    def read(self, model, id=None, *args, **kwargs):
        response = Collection(href=self.app.config.get('API_ROOT'))
        if self.database.get(model):
            response.template = self.models[model].get_collection_template()
            if id is None:
                for k, v in self.database[model].items():
                    response.items.append(v.get_collection_item())
            else:
                instance = self.database[model].get(id)
                if instance:
                    response.items.append(instance.get_collection_item())
                else:
                    abort(404)
            return response
        else:
            abort(404)

    def update(self, model, data, *args, **kwargs):
        response = Collection(href=self.app.config.get('API_ROOT'))
        try:
            data = Template(data)
        except (TypeError, ValueError, IndexError):
            abort(400)
        if self.database.get(model):
            response.template = self.database[model].get_collection_template()
            if self.database[model].get(id):
                instance = self.database[model][id]
                instance.update(data)
                self.__write_db_file()
                response.items.append(instance.get_collection_item())
                return response
            else:
                abort(404)
        else:
            abort(404)

    def delete(self, model, id=None, *args, **kwargs):
        if self.database.get(model):
            if self.database[model].get(id):
                del self.database[model][id]
                self.__write_db_file()
            else:
                abort(404)
        else:
            abort(404)

    def search(self, model, data, *args, **kwargs):
        pass