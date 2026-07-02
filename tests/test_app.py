"""Integration tests for the Flask calculator API."""

import json


def post_json(client, url, data):
    return client.post(url, data=json.dumps(data), content_type="application/json")


# ------------------------------------------------------------------
# Simple arithmetic endpoints
# ------------------------------------------------------------------


def test_add(client):
    resp = post_json(client, "/add", {"a": 3, "b": 4})
    assert resp.status_code == 200
    assert resp.get_json() == {"result": 7}


def test_subtract(client):
    resp = post_json(client, "/subtract", {"a": 10, "b": 3})
    assert resp.status_code == 200
    assert resp.get_json() == {"result": 7}


def test_multiply(client):
    resp = post_json(client, "/multiply", {"a": 6, "b": 7})
    assert resp.status_code == 200
    assert resp.get_json() == {"result": 42}


def test_divide(client):
    resp = post_json(client, "/divide", {"a": 10, "b": 4})
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 2.5


def test_divide_by_zero(client):
    resp = post_json(client, "/divide", {"a": 5, "b": 0})
    assert resp.status_code == 400
    body = resp.get_json()
    assert "detail" in body


# ------------------------------------------------------------------
# /calculations CRUD
# ------------------------------------------------------------------


def test_create_calculation_add(client):
    resp = post_json(client, "/calculations", {"operation": "add", "a": 1, "b": 2})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["operation"] == "add"
    assert body["a"] == 1
    assert body["b"] == 2
    assert body["result"] == 3
    assert "id" in body
    assert "created_at" in body


def test_create_calculation_unknown_operation(client):
    resp = post_json(client, "/calculations", {"operation": "mod", "a": 10, "b": 3})
    assert resp.status_code == 400
    assert "detail" in resp.get_json()


def test_create_calculation_div_by_zero(client):
    resp = post_json(client, "/calculations", {"operation": "div", "a": 5, "b": 0})
    assert resp.status_code == 400
    assert "detail" in resp.get_json()


def test_list_calculations(client):
    # Seed a record first
    post_json(client, "/calculations", {"operation": "mul", "a": 2, "b": 3})
    resp = client.get("/calculations")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_calculation_existing(client):
    create_resp = post_json(client, "/calculations", {"operation": "sub", "a": 9, "b": 4})
    calc_id = create_resp.get_json()["id"]

    resp = client.get(f"/calculations/{calc_id}")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["id"] == calc_id
    assert body["result"] == 5


def test_get_calculation_missing(client):
    resp = client.get("/calculations/99999")
    assert resp.status_code == 404
    assert "detail" in resp.get_json()


def test_delete_calculation(client):
    create_resp = post_json(client, "/calculations", {"operation": "add", "a": 1, "b": 1})
    calc_id = create_resp.get_json()["id"]

    del_resp = client.delete(f"/calculations/{calc_id}")
    assert del_resp.status_code == 204

    # Confirm it's gone
    get_resp = client.get(f"/calculations/{calc_id}")
    assert get_resp.status_code == 404


def test_delete_calculation_missing(client):
    resp = client.delete("/calculations/99999")
    assert resp.status_code == 404
    assert "detail" in resp.get_json()
