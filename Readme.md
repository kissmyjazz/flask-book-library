A test RESTful application allowing to borrow books from a library.

Written using Flask framework in Python and uses PosgtreSQL as a backend database

Tested with python 3.6

Application starts by running 


```
python run.py 
```

to create tables in a database, then

```
python run.py 
```

runs the server.

Some endpoints require authorisation.
Registration is done by sending username and password in the body of the HTTP request, e.g.

```
{
	"username": "name"
	"password": "strongpasswd"
}
```


Healthcheck is located at:

```
\healthcheck
```

Some test coverage can be done with Newman
https://github.com/postmanlabs/newman


```
newman run flask.postman_collection.json -e flask.postman_environment.json
```
