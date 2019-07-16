# jsonbox-api

A simple api to store json data.

`jsonbox-api` was developed to take advantage of certain "shared-hosts" that provides "unlimited" databases.
Usually, they are very cheap and not suitable for production, but "ok" for pet projects.


### Dependencies

* Python 3.7+
* Django 2.2+
* Mysql 5.7+
* pipenv

### Development

Create a virtualenv using your prefered method and install `pipenv`.

```bash
$ pipenv install --dev
$ cp local.env .env
$ # edit .env
$ cd jsonbox-api/
$ ./manage.py migrate
$ ./manage.py collectstatic --link
$ ./manage.py runserver
```

Running tests:

```bash
$ make test
$ make lint # pre-commit
$ make check-dead-fixtures # pytest-deadfixtures
```

### Commands

Available management commands:

* `box_create`: create a box instance
* `box_list`: list all boxes and the associated token


### License

[MIT](LICENSE)

### Similar projects

* [jsonbin](https://jsonbin.io/)
* [jsonstore](https://www.jsonstore.io/)
* [myjson](http://myjson.com/)
