"""Tests for the calculator operation endpoints (/add, /subtract, /multiply, /divide)."""

import pytest


class TestAddEndpoint:
    """Tests for POST /add."""

    def test_add_positive_integers(self, client):
        resp = client.post("/add", json={"a": 1, "b": 2})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 3.0}

    def test_add_negative_numbers(self, client):
        resp = client.post("/add", json={"a": -5, "b": -3})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": -8.0}

    def test_add_floats(self, client):
        resp = client.post("/add", json={"a": 1.5, "b": 2.3})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == pytest.approx(3.8)

    def test_add_zeros(self, client):
        resp = client.post("/add", json={"a": 0, "b": 0})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 0.0}


class TestSubtractEndpoint:
    """Tests for POST /subtract."""

    def test_subtract_positive_integers(self, client):
        resp = client.post("/subtract", json={"a": 10, "b": 3})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 7.0}

    def test_subtract_negative_result(self, client):
        resp = client.post("/subtract", json={"a": 3, "b": 10})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": -7.0}

    def test_subtract_floats(self, client):
        resp = client.post("/subtract", json={"a": 5.5, "b": 2.3})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == pytest.approx(3.2)


class TestMultiplyEndpoint:
    """Tests for POST /multiply."""

    def test_multiply_positive_integers(self, client):
        resp = client.post("/multiply", json={"a": 3, "b": 4})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 12.0}

    def test_multiply_by_zero(self, client):
        resp = client.post("/multiply", json={"a": 5, "b": 0})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 0.0}

    def test_multiply_negative_numbers(self, client):
        resp = client.post("/multiply", json={"a": -3, "b": -4})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 12.0}

    def test_multiply_floats(self, client):
        resp = client.post("/multiply", json={"a": 2.5, "b": 4.0})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == pytest.approx(10.0)


class TestDivideEndpoint:
    """Tests for POST /divide."""

    def test_divide_positive_integers(self, client):
        resp = client.post("/divide", json={"a": 10, "b": 2})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 5.0}

    def test_divide_floats(self, client):
        resp = client.post("/divide", json={"a": 7.5, "b": 2.5})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == pytest.approx(3.0)

    def test_divide_by_zero_returns_400(self, client):
        resp = client.post("/divide", json={"a": 10, "b": 0})
        assert resp.status_code == 400
        data = resp.get_json()
        assert "detail" in data
        assert data["detail"] == "Cannot divide by zero"

    def test_divide_negative_numbers(self, client):
        resp = client.post("/divide", json={"a": -10, "b": -2})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 5.0}

    def test_divide_zero_by_nonzero(self, client):
        resp = client.post("/divide", json={"a": 0, "b": 5})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 0.0}


class TestInputValidation:
    """Tests for input validation across all calculator endpoints."""

    def test_missing_json_body(self, client):
        resp = client.post("/add", content_type="application/json")
        assert resp.status_code == 400
        assert "detail" in resp.get_json()

    def test_missing_field_a(self, client):
        resp = client.post("/add", json={"b": 2})
        assert resp.status_code == 400
        data = resp.get_json()
        assert "detail" in data

    def test_missing_field_b(self, client):
        resp = client.post("/add", json={"a": 1})
        assert resp.status_code == 400
        data = resp.get_json()
        assert "detail" in data

    def test_non_numeric_field(self, client):
        resp = client.post("/add", json={"a": "abc", "b": 2})
        assert resp.status_code == 400
        data = resp.get_json()
        assert "detail" in data

    def test_string_encoded_numbers_are_accepted(self, client):
        """String-encoded numbers should be coerced to floats like Pydantic does."""
        resp = client.post("/add", json={"a": "3", "b": "2"})
        assert resp.status_code == 200
        assert resp.get_json() == {"result": 5.0}
