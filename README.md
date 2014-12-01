Flask-CRUDSDB
=============
An abstraction API for creating a CRUDS interface in python for accessing databases in Flask, with a focus on ReSTful
web APIs. Uses the [Collection+JSON hypermedia type](http://amundsen.com/media-types/collection/) for programmatically 
accessible representations of information.

This package is to serve as a framework for abstracting flask applications away from the type of database they use, to
improve portability of the flask application code.

Flask config options:
---
* `API_ROOT`: The root uri for your api endpoints, e.g., `'/api/'`
* `FLAT_DATABASE_FILE`: A file path where to store the database, only applies to `flatfile` module.

Included extensions:
---
* `flatfile`: A module for abstracting flatfile databases. Stores in configurable path as json.
* `sqlalchemy`: A module for abstracting SQLAlchemy databases. Uses normal Flask-SQLAlchemy configuration options.
* `couch_db`: A module for abstracting CouchDB databases. -- *Does nothing yet. Coming soon!*

Examples:
---
* [BlackBook](http://github.com/ievans3024/BlackBook) -- The project this framework spawned from.