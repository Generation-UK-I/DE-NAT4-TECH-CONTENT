# Running the app

FYI - On Windows you will need a GitBash terminal or to use WSL2.

## Create a venv

```sh
# Mac/Unix
$ python3 -m venv .venv
# or on Windows
$ py -m venv .venv
```

## Activate venv

Unix/MacOS:

```sh
# activate the virtual environment
$ source .venv/bin/activate
# deactivate the virtual environment (for after you are done)
$ deactivate
```

Windows:

```sh
# activate the virtual environment
$ .venv\Scripts\activate.bat
# deactivate the virtual environment (for after you are done)
$ deactivate
```

## Install dependencies

Run this to install the dependencies:

```sh
# Mac/Unix
$ python3 -m pip install -r requirements.txt
# or on Windows
$ py -m pip install -r requirements.txt
```

## Run flask

You need to run Flask not python directly. On Windows you will need a GitBash terminal:

```sh
$ export FLASK_APP=route
$ export FLASK_ENV=development
$ flask run
```

### Browse your root url

Browse to <http://localhost:5000/> and you should see the "Hello world" raw page.

## Open file

Open the `rest-ful-cafe.html` in your web browser.

The buttons in the web page should work now!
