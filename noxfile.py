"""Define sessions for nox tasks."""
import tempfile
from typing import Any

import nox
from nox.sessions import Session

locations = "config", "mysite", "manage.py", "noxfile.py"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session
def lint(session: Session) -> None:
    """Run linting tools to check code."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "black",
        "flake8",
        "flake8-django",
        "flake8-docstrings",
        "mypy",
        "django-environ",
        "whitenoise",
        "django-stubs",
    )
    session.run("isort", "--profile", "black", "mysite")
    session.run("black", *args)
    session.run("flake8", *args)
    session.run("mypy", "mysite")
