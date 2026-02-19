"""Tests for the calculator API endpoints."""

import pytest

from server import create_app


@pytest.fixture()
def app():
    """Create a test application with an in-memory database."""
    app = create_app(
        config_overrides={
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    """Create a test client."""
    return app.test_client()


# --- Addition Tests ---


class TestAddEndpoint:
    """Tests for POST /add."""

    def test_add_positive_numbers(self, client):
        """Test adding two positive numbers."""
        response = client.post("/add", json={"a": 2, "b": 3})
        assert response.status_code == 200
        assert response.get_json() == {"result": 5.0}

    def test_add_negative_numbers(self, client):
        """Test adding negative numbers."""
        response = client.post("/add", json={"a": -5, "b": -3})
        assert response.status_code == 200
        assert response.get_json() == {"result": -8.0}

    def test_add_float_numbers(self, client):
        """Test adding float numbers."""
        response = client.post("/add", json={"a": 1.5, "b": 2.5})
        assert response.status_code == 200
        assert response.get_json() == {"result": 4.0}

    def test_add_zero(self, client):
        """Test adding zero."""
        response = client.post("/add", json={"a": 5, "b": 0})
        assert response.status_code == 200
        assert response.get_json() == {"result": 5.0}


# --- Subtraction Tests ---


class TestSubtractEndpoint:
    """Tests for POST /subtract."""

    def test_subtract_positive_numbers(self, client):
        """Test subtracting two positive numbers."""
        response = client.post("/subtract", json={"a": 10, "b": 3})
        assert response.status_code == 200
        assert response.get_json() == {"result": 7.0}

    def test_subtract_resulting_negative(self, client):
        """Test subtraction resulting in a negative number."""
        response = client.post("/subtract", json={"a": 3, "b": 10})
        assert response.status_code == 200
        assert response.get_json() == {"result": -7.0}

    def test_subtract_floats(self, client):
        """Test subtracting float numbers."""
        response = client.post("/subtract", json={"a": 5.5, "b": 2.5})
        assert response.status_code == 200
        assert response.get_json() == {"result": 3.0}


# --- Multiplication Tests ---


class TestMultiplyEndpoint:
    """Tests for POST /multiply."""

    def test_multiply_positive_numbers(self, client):
        """Test multiplying two positive numbers."""
        response = client.post("/multiply", json={"a": 4, "b": 5})
        assert response.status_code == 200
        assert response.get_json() == {"result": 20.0}

    def test_multiply_by_zero(self, client):
        """Test multiplying by zero."""
        response = client.post("/multiply", json={"a": 7, "b": 0})
        assert response.status_code == 200
        assert response.get_json() == {"result": 0.0}

    def test_multiply_negative_numbers(self, client):
        """Test multiplying negative numbers."""
        response = client.post("/multiply", json={"a": -3, "b": -4})
        assert response.status_code == 200
        assert response.get_json() == {"result": 12.0}

    def test_multiply_floats(self, client):
        """Test multiplying float numbers."""
        response = client.post("/multiply", json={"a": 2.5, "b": 4})
        assert response.status_code == 200
        assert response.get_json() == {"result": 10.0}


# --- Division Tests ---


class TestDivideEndpoint:
    """Tests for POST /divide."""

    def test_divide_positive_numbers(self, client):
        """Test dividing two positive numbers."""
        response = client.post("/divide", json={"a": 10, "b": 2})
        assert response.status_code == 200
        assert response.get_json() == {"result": 5.0}

    def test_divide_resulting_float(self, client):
        """Test division resulting in a float."""
        response = client.post("/divide", json={"a": 7, "b": 2})
        assert response.status_code == 200
        assert response.get_json() == {"result": 3.5}

    def test_divide_by_zero(self, client):
        """Test division by zero returns 400 error."""
        response = client.post("/divide", json={"a": 10, "b": 0})
        assert response.status_code == 400
        data = response.get_json()
        assert "detail" in data
        assert "Cannot divide by zero" in data["detail"]

    def test_divide_negative_numbers(self, client):
        """Test dividing negative numbers."""
        response = client.post("/divide", json={"a": -10, "b": 2})
        assert response.status_code == 200
        assert response.get_json() == {"result": -5.0}


# --- Validation Error Tests ---


class TestValidationErrors:
    """Tests for input validation errors across all endpoints."""

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_missing_field_a(self, client, endpoint):
        """Test that missing 'a' field returns validation error."""
        response = client.post(endpoint, json={"b": 5})
        assert response.status_code == 400
        data = response.get_json()
        assert "errors" in data
        assert "a" in data["errors"]

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_missing_field_b(self, client, endpoint):
        """Test that missing 'b' field returns validation error."""
        response = client.post(endpoint, json={"a": 5})
        assert response.status_code == 400
        data = response.get_json()
        assert "errors" in data
        assert "b" in data["errors"]

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_missing_both_fields(self, client, endpoint):
        """Test that missing both fields returns validation errors."""
        response = client.post(endpoint, json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "errors" in data
        assert "a" in data["errors"]
        assert "b" in data["errors"]

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_non_numeric_field_a(self, client, endpoint):
        """Test that non-numeric 'a' field returns validation error."""
        response = client.post(endpoint, json={"a": "abc", "b": 5})
        assert response.status_code == 400
        data = response.get_json()
        assert "errors" in data
        assert "a" in data["errors"]

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_non_numeric_field_b(self, client, endpoint):
        """Test that non-numeric 'b' field returns validation error."""
        response = client.post(endpoint, json={"a": 5, "b": "xyz"})
        assert response.status_code == 400
        data = response.get_json()
        assert "errors" in data
        assert "b" in data["errors"]

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_empty_body(self, client, endpoint):
        """Test that an empty request body returns validation errors."""
        response = client.post(endpoint, content_type="application/json")
        assert response.status_code == 400

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_response_json_structure(self, client, endpoint):
        """Test that successful responses have correct JSON structure."""
        response = client.post(endpoint, json={"a": 6, "b": 3})
        assert response.status_code == 200
        data = response.get_json()
        assert "result" in data
        assert isinstance(data["result"], (int, float))
