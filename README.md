# VCERP PDV System

VCERP PDV System is a web application built with [Django](https://www.djangoproject.com/) aimed at managing
inventory, clients and the daily cash register of a business.  The project
is organized as a standard Django project with two primary applications:
`vcerp_estoque` (inventory and general ERP features) and `vcerp_caixa` (point of
sale / cash register).

## Features

- **Inventory management** – products, contracts and transaction tracking.
- **Client management** – support for individuals (`PessoaFisica`) and
  companies (`PessoaJuridica`).
- **Cash register control** – open/close cash boxes and log operations.
- **User authentication** – login, registration and profile management.

The main apps are registered in `INSTALLED_APPS` inside the Django settings:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vcerp_estoque',
    'vcerp_caixa',
]
```

_Source: [`vcerp_principal/vcerp_principal/settings.py`](vcerp_principal/vcerp_principal/settings.py)_

## Requirements

This project was generated using Django 5.1 but the repository also contains a
Windows virtual environment with Django 4.1. To run the project, create a fresh
virtual environment with Python 3.11+ and install Django:

```bash
python -m venv .venv
source .venv/bin/activate
pip install django
```

Additional packages may be required depending on the features you use.

## Running

From the repository root, run the usual Django development server:

```bash
python vcerp_principal/manage.py migrate
python vcerp_principal/manage.py runserver
```

The application uses SQLite by default (see `DATABASES` in `settings.py`).

## Testing

Unit tests can be executed with:

```bash
python vcerp_principal/manage.py test
```

Note that the repository contains no test implementation yet.

## Project Structure

```
VCERP_PDV-system/
├── vcerp_principal/      # Django project and apps
│   ├── vcerp_caixa/      # Cash register module
│   └── vcerp_estoque/    # Inventory and ERP module
└── venv/                 # Windows virtual environment (not required)
```

## License

No explicit license was found in the repository. Please consult the project
owner before using it in production.
