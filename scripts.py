from subprocess import check_call


def start() -> None:
    check_call(
        [
            "poetry",
            "run",
            "gunicorn",
            "--bind",
            "127.0.0.1:5000",
            "main:app",
            "-e",
            "FLASK_ENV=development",
        ]
    )
