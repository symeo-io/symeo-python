Symeo Python SDK
================

The Symeo SDK made for interacting with your Symeo secrets and configuration from python applications.

.. figure:: https://circleci.com/gh/symeo-io/symeo-python.svg?style=svg
    :target: https://circleci.com/gh/symeo-io/symeo-python

.. figure:: _static/github-mark.svg
    :target: https://github.com/symeo-io/symeo-python
    :width: 50px

Installation
------------

Pip
~~~

Add ``symeo-python`` to your ``requirements.txt``

..  code-block:: python

    symeo-python==0.0.1


Run

..  code-block:: shell

    pip install -r requirements.txt

Or run directly

..  code-block:: shell

    pip install symeo-python

Pipenv
~~~~~~


Add ``symeo-python`` to your ``Pipfile``

..  code-block:: python

    [packages]
    symeo-python = "0.0.1"


Run

..  code-block:: shell

    pipenv install

Usage
-----

Define configuration contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``symeo.config.yml`` file in the root of your project, and define the structure and types of your application configuration:

..  code-block:: yaml

    aws:
      region:
         type: string
      database:
         host:
            type: string
         port:
            type: integer
         username:
            type: string
         password:
            type: string

- You can nest properties to any depth level
- Supported types are string and integer

Build Config class from the contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To generate the ``Config`` class corresponding to your contract, run the command :

.. code-block:: shell

    $ symeo-python build

Create your local configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``symeo.local.yml`` file in the root of your project, defining the values matching your configuration contract:

..  code-block:: yaml

    aws:
      region: eu-west-3
      database:
         host: localhost
         port: 5432
         username: postgres
         password: XPJc5qAbQcn77GWg


Use your configuration anywhere in your code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your configuration is then accessible with the import:

..  code-block:: python

    from symeo_python.config import config


For example:

..  code-block:: python

    from symeo_python.config import config
    from psycopg2 import pool


    class DatabaseClient:
        def __init__(self):
            self.connection_pool = pool.SimpleConnectionPool(
                1,
                3,
                host=config.database.host,
                port=config.database.port,
                user=config.database.user,
                password=config.database.password,
            )


Wrap your application startup with the symeo command
----------------------------------------------------

Local run
~~~~~~~~~

To run locally your application using the configuration values file ``symeo.local.yml``, you have to wrap your command to start your application with the ``symeo-python`` cli :

.. code-block:: shell

    $ symeo-python start -- $your_command_to_start_your_application

1. Example 1 with ``uvicorn``

.. code-block:: shell

    $ symeo-python start -- uvicorn main:app


2. Example 2 with a simple python ``main.py``

.. code-block:: shell

    $ symeo-python start -- python main.py


Custom values file
~~~~~~~~~~~~~~~~~~

You can specify the path and name of the local file with the ``-f`` flag:

.. code-block:: shell

    $ symeo-python start -f symeo.local.yml -- $your_command_to_start_your_application


Start application with configuration from Symeo platform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After creating an environment and its api key in the [Symeo platform](https://app-config-staging.symeo.io/), run

.. code-block:: shell

    $ symeo-python start -k $YOUR_ENVIRONMENT_API_KEY -- uvicorn main:app


So the sdk fetch the values for the given environment and starts your application with those values.

Follow the [Symeo platform documentation](https://symeo.io/) for more details.

Help
====

To get some help with the CLI, please use the following commands :

.. code-block:: shell

    $ symeo-python build --help

or

.. code-block:: shell

    $ symeo-python start --help
