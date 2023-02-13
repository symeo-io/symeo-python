# Symeo Python SDK

The Symeo SDK made for interacting with your Symeo secrets and configuration from python applications.

# Install

## Pip

Add `symeo-python` to your `requirements.txt`

Ex :
```t
symeo-python==0.0.1
```

Run `pip install -r requirements.txt`

Or run directly `pip install symeo-python`

## Pipenv


Add `symeo-python` to your `Pipfile`

Ex :
```
[packages]
symeo-python = "0.0.1"
```

Run `pipenv install`

# Usage

## Define configuration contract

Create a `symeo.config.yml` file in the root of your project, and define the structure and types of your application configuration:

```yaml
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
```

- You can nest properties to any depth level
- Supported types are boolean, string, integer and float

## Create your local configuration file

Create a `symeo.local.yml` file in the root of your project, defining the values matching your configuration contract:

```yaml
aws:
  region: eu-west-3
  database:
    host: localhost
    port: 5432
    username: postgres
    password: XPJc5qAbQcn77GWg
```

## Use your configuration anywhere in your code

Your configuration is then accessible with the import:

```python
from symeo_python.config import config
```

For example:

```python
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
```

## Wrap your application startup with the symeo command


### Custom contract file

You can specify the path and name of the local file with the `-f` flag:

```shell
$ symeo-python start -f symeo.local.yml -- uvicorn main:app
```

### Start application with configuration from Symeo platform

After creating an environment and its api key in the [Symeo platform](https://app-config-staging.symeo.io/), run

```shell
$ symeo-python start -k $YOUR_ENVIRONMENT_API_KEY -- uvicorn main:app
```

So the sdk fetch the values for the given environment and starts your application with those values.

Follow the [Symeo platform documentation](https://symeo.io/) for more details.

# Help

To get some help with the CLI, please use the following commands :

`symeo-python build --help`
or
`symeo-python start --help`
