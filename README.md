# Knowledge base
Simple django/angular application that allows to share information in a group of users.


## Prerequisites
+ [Oracle's VirtualBox](https://www.virtualbox.org/)
+ [Vagrant](http://www.vagrantup.com/)
+ [Python](http://www.python.org/)
+ [Fabric](http://www.fabfile.org/)
+ [fabutils](https://github.com/vinco/fabutils)


## Configuring your virtual environment
1. Fork the repo with your Github's user

2. Clone your fork

    ```bash
    $ git clone --recursive git@github.com:{ your username  }/redsep.git
    ```

3. Create the virtual machine

    ```bash
    $ cd redsep
    $ vagrant up
    ```
4.  Development environment configuration for localhost to work in redsep.local

    ```bash
    # /etc/hosts
    192.168.33.23       redsep.local
    ```

5. Build the environment inside the virtual machine

    ```bash
    $ fab environment:vagrant bootstrap
    ```

6. Run the development server

```
    $ fab environment:vagrant runserver
    ```

6. Open your web browser and check the project at `redsep.local`


## Useful fabric commands

### makemigrations \[app\]\[,options\]
Create new migrations based on the changes detected in the project's model. [\[\+\]](https://docs.djangoproject.com/en/1.8/ref/django-admin/#django-admin-makemigrations)
```bash
# Creating migrations for the whole project
$ fab environment:vagrant makemigrations

# Creating migrations for a specific app
$ fab environment:vagrant makemigrations:some_app

# Passing options to the command
$ fab environment:vagrant makemigrations:some_app,empty=true
```

### migrate \[app \[,migration\]\]\[,options\]
Sync the database with the current set of models and migrations. [\[\+\]](https://docs.djangoproject.com/en/1.8/ref/django-admin/#migrate)
```bash
# Syncing the whole project
$ fab environment:vagrant migrate

# Syncing a specific app
$ fab environment:vagrant migrate:some_app

# Syncing a specific app to a specific migration state
$ fab environment:vagrant migrate:some_app,0001

# Passing options to the command
$ fab environment:vagrant migrate:some_app,0001,fake=true
```

### resetdb
Drop and rebuild a fresh database instance for the project.
```bash
$ fab environment:vagrant resetdb
```

### install_requirements
Install the Python dependencies for the project specified in the proper requirements file for the given environment.
```bash
# Installing dependencies
$ fab environment:vagrant install_requirements

# Install and upgrading dependencies
$fab environment:vagrant install_requirements:upgrade=True
```


### runserver
Run the development server inside the virtual machine.
```bash
$ fab environment:vagrant runserver
```

### maintenance \[on|off\]
Put the previously selected production/staging environment in maintenance mode
(on) or bring it back to serve the application (off).
Note that when the environment is in maintenance mode it will return an `HTTP
503` code to all requests and show a temporary placeholder page. This page must
be located at `maintenance/index.html` and can only reference assets from the
`maintenance/assets` directory.
```bash
# Activate maintenance mode in staging environment
$ fab environment:staging maintenance:on

# Deactivate maintenance mode in staging environment
$ fab environment:staging maintenance:off
```

### deploy \[reference\]\[,upgrade=boolean\]
Deploy the code from the given git reference (a branch or commit) to the
previously selected production/staging environment.
```bash
# Deploy to staging environment from commit abcdefg
$ fab environment:staging deploy:abcdefg

# Deploy to production environment from master branch
$ fab environment:production deploy:master

# Tell to the deploy task to upgrade the project's requirements during the
# deployment process
$ fab environment:production deploy:master,upgrade=true
```

## Fixtures

1. Loads the proper information from fixtures for development environment

    ```bash
    fab environment:vagrant load_dummy_data
    ```

2. Loads the proper information from fixtures for production environment (this information is necessary for the functioning of the system)

    ```bash
    fab environment:vagrant load_mandatory_dummy_data
    ```

# Testing

1. Open vagrant environment from ssh:
    ```bash
    $ vagrant ssh
    ```

2. Change directory to `/vagrant`:
    ```bash
    $ cd /vagrant
    ```

3. Install tox inside the virtual machine:
    ```bash
    $ pip install tox
    ```

4. Run the proper command with tox:

```
# Run the full test suite including the PEP8 linter.
$ tox

# Run only the PEP8 linter.
$ tox -e py27-flake8

# Run only the test suite.
$ tox -e py27-django

# Pass -r flag to recreate the virtual environment when requirements changes.
$ tox -r

# Run the test suite to a specific file.
$ tox -e py27-django src/redsep/core/api/tests/test_serializers.py
```
