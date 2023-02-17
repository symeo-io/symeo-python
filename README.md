<h1 align="center">
<a href="https://app-staging.symeo.io/">
  <img width="300" src="https://s3.eu-west-3.amazonaws.com/symeo.io-assets/symeo-logo.png" alt="symeo">
</a>
</h1>
<p align="center">
  <p align="center">Apps configuration as code. Easy. Centralized. Secured.</p>
</p>


<h4 align="center">
  <a href="https://app-staging.symeo.io/">SaaS</a> |
  <a href="https://symeoiomain-pivotconfiguration.gatsbyjs.io/">Website</a> |
  <a href="https://symeoiomain-pivotconfiguration.gatsbyjs.io/">Docs</a>
</h4>

<h4 align="center">
  <a href="https://github.com/medusajs/medusa/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-Apache-blue.svg" />
  </a>
 <a href="https://circleci.com/gh/symeo-io/symeo-python">
    <img src="https://circleci.com/gh/symeo-io/symeo-python.svg?style=svg"/>
 </a>

</h4>

# Symeo Python SDK

The Symeo SDK made for interacting with your Symeo secrets and configuration from python applications.

#  Installation

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
- Supported types are string and integer

## Build Config class from the contract

Generate the `Config` class corresponding to your contract using the following command :

`symeo-python build`

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

### Create your local configuration file

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
**Hint** : your can add your `symeo.local.yml` into your `.gitignore`

### Local run

To run locally your application using the configuration values file `symeo.local.yml`, you have to wrap your command to start your application with the `symeo-python` cli :

`symeo-python start -- $your_command_to_start_your_application`

1. Example 1 with `uvicorn`
```shell
symeo-python start -- uvicorn main:app
```

2. Example 2 with a simple python `main.py`

```shell
symeo-python start -- python main.py
```

### Custom values file

You can specify the path and name of the local file with the `-f` flag:

```shell
$ symeo-python start -f symeo.local.yml -- $your_command_to_start_your_application
```

### Start application with configuration from Symeo platform

After creating an environment and its api key in the [Symeo platform](https://app-config-staging.symeo.io/), run

```shell
$ symeo-python start -k $YOUR_ENVIRONMENT_API_KEY -- uvicorn main:app
```

So the sdk fetch the values for the given environment and starts your application with those values.

Follow the [Symeo platform documentation](https://symeo.io/) for more details.

## Symeo CLI options

### Options for the `build` command

`-c, --contract-file`

The path to your configuration contract file. Default is `symeo.config.yml`.

### Options for the `start` command

`-c, --contract-file`

The path to your configuration contract file. Default is `symeo.config.yml`.

`-f, --values-file`

The path to your local values file. Default is `symeo.local.yml`.

`-k, --api-key`

The environment api key to use to fetch values from Symeo platform. If empty, values will be fetched from local value file (`symeo.local.yml` by default). If specified, parameter `-f, --values-file` is ignored.

`-a, --api-url`

The api endpoint used to fetch your configuration with the api key. Default is `https://api-staging.symeo.io/api/v1/values`.


# Help

To get some help with the CLI, please use the following commands :

`symeo-python build --help`
or
`symeo-python start --help`
