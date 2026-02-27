"""A simple calculator REST API server built with Flask."""

import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from core import add, divide, multiply, subtract

# --- App & Configuration ---

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///calculator.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "0") == "1"

db = SQLAlchemy(app)

# --- Models ---


class Calculation(db.Model):  # type: ignore[name-defined]
    """Database model for stored calculations."""

    __tablename__ = "calculation"

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(10), nullable=False)
    a = db.Column(db.Float, nullable=False)
    b = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# --- Operations Dispatch ---

OPERATIONS: dict[str, callable] = {  # type: ignore[type-arg]
    "add": add,
    "sub": subtract,
    "mul": multiply,
    "div": divide,
}


# --- Request Validation Helper ---


def parse_calculation_request():
    """Parse and validate a JSON request body with 'a' and 'b' float fields.

    Returns:
        tuple: (a, b) as floats.

    Raises:
        ValueError: If the request body is missing, or 'a'/'b' are absent or not numeric.
    """
    data = request.get_json(silent=True)
    if data is None:
        raise ValueError("Request body must be valid JSON")

    if "a" not in data or "b" not in data:
        raise ValueError("Missing required fields: 'a' and 'b'")

    try:
        a = float(data["a"])
        b = float(data["b"])
    except (TypeError, ValueError):
        raise ValueError("Fields 'a' and 'b' must be numeric")

    return a, b


# --- Calculator Endpoints ---


@app.post("/add")
def api_add():
    """Add two numbers."""
    try:
        a, b = parse_calculation_request()
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400
    return jsonify({"result": add(a, b)})


@app.post("/subtract")
def api_subtract():
    """Subtract b from a."""
    try:
        a, b = parse_calculation_request()
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400
    return jsonify({"result": subtract(a, b)})


@app.post("/multiply")
def api_multiply():
    """Multiply two numbers."""
    try:
        a, b = parse_calculation_request()
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400
    return jsonify({"result": multiply(a, b)})


@app.post("/divide")
def api_divide():
    """Divide a by b."""
    try:
        a, b = parse_calculation_request()
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400
    try:
        result = divide(a, b)
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400
    return jsonify({"result": result})


# --- Database Initialization ---

with app.app_context():
    db.create_all()


# --- Entry Point ---

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    app.run(host=host, port=port)
