"""Shared pytest fixtures for the calculator API test suite."""

import pytest

from app import app as flask_app
from app import db


@pytest.fixture
def client():
    """Create a Flask test client with an in-memory SQLite database.

    Yields a test client that can be used to make requests to the app.
    The database is created fresh for each test and torn down afterwards.
    """
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with flask_app.app_context():
        db.create_all()
        yield flask_app.test_client()
        db.drop_all()
