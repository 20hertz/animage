from subprocess import check_call


def start() -> None:
    check_call(["poetry", "run", "gunicorn", "main:app", "-e", "FLASK_ENV=development"])
