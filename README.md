## Prerequisites
You need
- Python 3.7.3
- [Poetry](https://python-poetry.org/docs/#installation)
  
## Getting started
Create your virtual environment:
```sh
$ poetry install
```

Run the development server
```
$ poetry run flask run
```

Test
```sh
$ poetry run pytest
```

Run test formatter
```sh
$ poetry run black . --check
```

```sh
$ curl -F 'image=@/Users/stephane/Documents/kitty.jpg' http://127.0.0.1:5000
```