# Billing

## Initial setup
* Clone project - `git clone git@github.com:artinnok/billing.git`
* Install [virtualenv](https://virtualenv.pypa.io/en/stable/) and activate it
* Install Python packages for project - `pip install -r requirements.txt`
* Fill and create `src/config.env` with this keys:
    * SECRET_KEY - secret key for project, you can generate it [here](https://www.miniwebtool.com/django-secret-key-generator/)
    * DB_HOST - PostgreSQL database host, usually `localhost`
    * DB_NAME - PostgreSQL database name
    * DB_USER - PostgreSQL user
    * DB_PASSWORD - PostgreSQL password for user

    For example:
    ```
    SECRET_KEY=supersecret
    DB_HOST=localhost
    DB_NAME=foo
    DB_USER=bar
    DB_PASSWORD=foobarpass
    ```
* Migrate - `python manage.py migrate`
* Also, project shipped with [fixtures](https://docs.djangoproject.com/en/1.11/howto/initial-data/) and you can load them - `python manage.py loaddata core.json`
* Run server and enjoy! - `python manage.py runserver`