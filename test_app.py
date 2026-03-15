"""Tests for the Flask calculator API arithmetic endpoints."""

import pytest

from app import create_app


@pytest.fixture
def app():
    """Create a test application with an in-memory database."""
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        }
    )
    yield application


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


# --- /add endpoint ---


class TestAdd:
    """Tests for the /add endpoint."""

    def test_add_integers(self, client):
        response = client.post("/add", json={"a": 2, "b": 3})
        assert response.status_code == 200
        assert response.get_json() == {"result": 5.0}

    def test_add_floats(self, client):
        response = client.post("/add", json={"a": 1.5, "b": 2.5})
        assert response.status_code == 200
        assert response.get_json() == {"result": 4.0}

    def test_add_negative_numbers(self, client):
        response = client.post("/add", json={"a": -5, "b": 3})
        assert response.status_code == 200
        assert response.get_json() == {"result": -2.0}

    def test_add_zeros(self, client):
        response = client.post("/add", json={"a": 0, "b": 0})
        assert response.status_code == 200
        assert response.get_json() == {"result": 0.0}


# --- /subtract endpoint ---


class TestSubtract:
    """Tests for the /subtract endpoint."""

    def test_subtract_basic(self, client):
        response = client.post("/subtract", json={"a": 10, "b": 4})
        assert response.status_code == 200
        assert response.get_json() == {"result": 6.0}

    def test_subtract_negative_result(self, client):
        response = client.post("/subtract", json={"a": 3, "b": 10})
        assert response.status_code == 200
        assert response.get_json() == {"result": -7.0}


# --- /multiply endpoint ---


class TestMultiply:
    """Tests for the /multiply endpoint."""

    def test_multiply_basic(self, client):
        response = client.post("/multiply", json={"a": 3, "b": 5})
        assert response.status_code == 200
        assert response.get_json() == {"result": 15.0}

    def test_multiply_by_zero(self, client):
        response = client.post("/multiply", json={"a": 100, "b": 0})
        assert response.status_code == 200
        assert response.get_json() == {"result": 0.0}

    def test_multiply_negative(self, client):
        response = client.post("/multiply", json={"a": -3, "b": 4})
        assert response.status_code == 200
        assert response.get_json() == {"result": -12.0}


# --- /divide endpoint ---


class TestDivide:
    """Tests for the /divide endpoint."""

    def test_divide_basic(self, client):
        response = client.post("/divide", json={"a": 10, "b": 2})
        assert response.status_code == 200
        assert response.get_json() == {"result": 5.0}

    def test_divide_float_result(self, client):
        response = client.post("/divide", json={"a": 7, "b": 2})
        assert response.status_code == 200
        assert response.get_json() == {"result": 3.5}

    def test_divide_by_zero(self, client):
        response = client.post("/divide", json={"a": 10, "b": 0})
        assert response.status_code == 400
        data = response.get_json()
        assert "detail" in data
        assert "Cannot divide by zero" in data["detail"]


# --- Input validation ---


class TestValidation:
    """Tests for request validation across all endpoints."""

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_missing_field_a(self, client, endpoint):
        response = client.post(endpoint, json={"b": 3})
        assert response.status_code == 400

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_missing_field_b(self, client, endpoint):
        response = client.post(endpoint, json={"a": 3})
        assert response.status_code == 400

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_empty_body(self, client, endpoint):
        response = client.post(endpoint, json={})
        assert response.status_code == 400

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_invalid_type(self, client, endpoint):
        response = client.post(endpoint, json={"a": "not_a_number", "b": 3})
        assert response.status_code == 400

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_no_json_body(self, client, endpoint):
        response = client.post(endpoint, content_type="application/json")
        assert response.status_code == 400
