#!/usr/bin/env python3
"""A very simple calculator REST API server."""

from datetime import datetime

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError, fields

from core import add, divide, multiply, subtract

# --- Extension Instances ---

db = SQLAlchemy()
ma = Marshmallow()

# --- Operations Dispatch Map ---

OPERATIONS: dict[str, callable] = {  # type: ignore[type-arg]
    "add": add,
    "sub": subtract,
    "mul": multiply,
    "div": divide,
}

# --- Schemas ---


class CalculationRequestSchema(ma.Schema):  # type: ignore[name-defined]
    """Schema for calculator endpoint requests."""

    a = fields.Float(required=True)
    b = fields.Float(required=True)


calc_request_schema = CalculationRequestSchema()


# --- App Factory ---


def create_app(config_overrides: dict | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Default configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calculator.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Apply any overrides (useful for testing)
    if config_overrides:
        app.config.update(config_overrides)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # --- Error Handlers ---

    @app.errorhandler(ValidationError)
    def handle_validation_error(err: ValidationError):  # type: ignore[type-arg]
        """Return JSON for marshmallow validation errors."""
        return jsonify({"errors": err.messages}), 400

    @app.errorhandler(400)
    def handle_bad_request(err):  # type: ignore[type-arg]
        """Return JSON for 400 errors."""
        description = getattr(err, "description", "Bad request")
        return jsonify({"detail": description}), 400

    @app.errorhandler(404)
    def handle_not_found(err):  # type: ignore[type-arg]
        """Return JSON for 404 errors."""
        description = getattr(err, "description", "Not found")
        return jsonify({"detail": description}), 404

    # --- Calculator Endpoints ---

    @app.post("/add")
    def add_route():  # type: ignore[type-arg]
        """Add two numbers."""
        data = calc_request_schema.load(request.get_json(silent=True) or {})
        result = add(data["a"], data["b"])
        return jsonify({"result": result})

    @app.post("/subtract")
    def subtract_route():  # type: ignore[type-arg]
        """Subtract b from a."""
        data = calc_request_schema.load(request.get_json(silent=True) or {})
        result = subtract(data["a"], data["b"])
        return jsonify({"result": result})

    @app.post("/multiply")
    def multiply_route():  # type: ignore[type-arg]
        """Multiply two numbers."""
        data = calc_request_schema.load(request.get_json(silent=True) or {})
        result = multiply(data["a"], data["b"])
        return jsonify({"result": result})

    @app.post("/divide")
    def divide_route():  # type: ignore[type-arg]
        """Divide a by b."""
        data = calc_request_schema.load(request.get_json(silent=True) or {})
        try:
            result = divide(data["a"], data["b"])
        except ValueError as e:
            return jsonify({"detail": str(e)}), 400
        return jsonify({"result": result})

    return app


def main() -> None:
    """Run the server."""
    app = create_app()
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
