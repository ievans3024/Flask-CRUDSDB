__author__ = 'Ian S. Evans'
"""
CRUDS Database abstraction system
http://github.com/ievans3024/Flask-CRUDSDB
"""


class Database(object):
    """
    A base class for database abstraction for ReSTful APIs

    This class is a skeleton to model wrappers from. A database wrapper should abstract away database/ORM quirks in
    behind a simple interface modeled after CRUDS -- Create, Read, Update, Delete, Search -- systems.

    Subclass this class when creating a new wrapper class. Implement the same methods provided here, and the application
    code will be able to interact with the database regardless of what kind of database is being used.
    """

    class Model(object):
        """
        A base class for database models.

        This class is a skeleton to model information models from. A database wrapper may subclass this to provide
        some simple methods for different kinds of information.

        When an information model inherits from this and another class, this class should be to the right of all other
        inherited classes, e.g:
            class SomeMultiInheritModel(SomeOtherModel, Model):
                pass
        """

        class ModelError(BaseException):
            """
            Wrapper class for model-specific errors. Can be subclassed.
            Purely exists to allow for catching explicitly written model errors (e.g., for data validation) and to
            create custom exceptions to catch different types of errors (e.g., missing required fields, wrong data
            type, etc.)
            """
            def __init__(self, message, *args, **kwargs):
                super(BaseException, self).__init__(message)

        def __init__(self, data, *args, **kwargs):
            """
            Model Constructor
            All models should implement this method.
            This method should raise a Database.Model.ModelError or a subclass of it when data supplied is invalid.
            Models should have an 'endpoint' property that can be set on init
            :param data: The data to populate this instance with
            :type data: collection_json.Template
            :return:
            """
            # TODO: Change this to a pass statement? Print a warning in console?
            raise NotImplementedError()

        def get_collection_item(self, as_dict=False):
            """
            Get a collection_json.Item representation of this model
            :param as_dict: If true, return a dict-like object instead of a collection_json.Item instance.
            :return: A collection_json.Item instance by default, a dict-like object if as_dict is true.
            """
            raise NotImplementedError()

        @staticmethod
        def get_template(as_dict=False):
            """
            Get an empty collection_json.Template for this model
            :param as_dict: If true, return a dict-like object instead of a collection_json.Template instance.
            :return: A collection_json.Template instance by default, a dict-like object if as_dict is true
            """
            raise NotImplementedError()

        def update(self, data):
            """
            Update this model instance's data
            :param data: The information to update the model with.
            :type data: collection_json.Template
            :return:
            """
            raise NotImplementedError()

    def __init__(self, app, *args, **kwargs):
        """
        Database Constructor
        All Databases should implement this method.
        All Databases should create a property called "models" that is a dict-like object where keys are the model name
        and values are the Model Class, e.g.:
            self.models = {
                'ModelOne': SomeDatabaseClass.ModelOne,
                'ModelTwo': SomeDatabaseClass.ModelTwo
            }
        :param app: The flask application to tie this Database to.
        :param args:
        :param kwargs:
        :return:
        """
        self.app = app
        self.models = {}

    def add_model(self, model_class):
        """
        Add a model class to the instance models.
        :param model_class: The model class to add
        :type model_class: database.Database.Model
        :raises TypeError: If model_class is not a subclass of flask_crudsdb.Database.Model
        :return:
        """
        if issubclass(model_class, Database.Model):
            try:
                self.models[model_class.__name__] = model_class
            except (AttributeError, TypeError):
                raise NotImplementedError(
                    self.__class__.__name__ + ' does not have a "models" attribute or it is not subscriptable.'
                )
        else:
            raise TypeError('model_class must be a subclass of flask_crudsdb.Database.Model')

    def create(self, model, data, *args, **kwargs):
        """
        Create a new model instance.
        Please note that server-side data validation should happen in the model's init method somewhere.
        This method should capture instances of Database.Model.ModelError and return a Collection containing the
        appropriate error information.
        :param model: The model to create a new instance of.
        :param data: The data to parse into the model.
        :return: A collection_json.Collection instance containing information about what happened (including errors.)
        """
        raise NotImplementedError()

    def read(self, model, *args, **kwargs):
        """
        Get information representing a model instance.
        :param model: The model to attempt to read from, using information in args/kwargs to specify what is requested.
        :return: A collection_json.Collection instance containing information about the requested resource or what
        happened (including errors.)
        """
        raise NotImplementedError()

    def update(self, model, data, *args, **kwargs):
        """
        Update information for an existing model instance.
        Please note that server-side data validation should happen in the model's init method somewhere.
        This method should capture instances of Database.Model.ModelError and return a Collection containing the
        appropriate error information.
        :param model: The model to update the information for.
        :param data: The data to parse into the model. Should accept partial data and overlay it on existing data.
        :return: A collection_json.Collection instance containing information about what happened (including errors.)
        """
        raise NotImplementedError()

    def delete(self, model, *args, **kwargs):
        """
        Delete an instance of a model.
        This method should determine from args/kwargs which instance of the model to delete.
        :param model: The model to delete an instance of.
        :return: A collection_json.Collection instance containing information about what happened (including errors.)
        """
        raise NotImplementedError()

    def search(self, model, data, *args, **kwargs):
        """
        Search a model for instances that might be relevant to a query.
        :param model: The model to search through instances of.
        :return: A collection_json.Collection instance containing information about the results from the query, or about
        what happened (including errors.)
        """
        raise NotImplementedError()