#!/usr/bin/env python3
"""A very simple calculator REST API server."""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields

from core import add, divide, multiply, subtract

# --- Extensions (initialized in create_app) ---

db = SQLAlchemy()

# --- Marshmallow Schemas ---


class CalculationRequestSchema(Schema):
    """Schema for arithmetic endpoint request bodies."""

    a = fields.Float(required=True)
    b = fields.Float(required=True)


class ResultResponseSchema(Schema):
    """Schema for arithmetic endpoint responses."""

    result = fields.Float(required=True)


# Schema instances
calculation_request_schema = CalculationRequestSchema()
result_response_schema = ResultResponseSchema()

# --- Operations map ---

OPERATIONS: dict[str, callable] = {  # type: ignore[type-arg]
    "add": add,
    "sub": subtract,
    "mul": multiply,
    "div": divide,
}


# --- Application Factory ---


def create_app(config=None):
    """Create and configure the Flask application.

    Args:
        config: Optional dictionary of configuration overrides.

    Returns:
        Configured Flask application instance.
    """
    application = Flask(__name__)

    # Default configuration
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calculator.db"
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Override with provided config
    if config:
        application.config.update(config)

    # Initialize extensions
    db.init_app(application)

    # Create tables
    with application.app_context():
        db.create_all()

    # --- Global error handler for marshmallow ValidationError ---

    @application.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Return 400 JSON response for marshmallow validation errors."""
        return jsonify({"detail": error.messages}), 400

    # --- Calculator Endpoints ---

    @application.route("/add", methods=["POST"])
    def api_add():
        """Add two numbers."""
        data = calculation_request_schema.load(request.get_json())
        result = add(data["a"], data["b"])
        return jsonify(result_response_schema.dump({"result": result}))

    @application.route("/subtract", methods=["POST"])
    def api_subtract():
        """Subtract b from a."""
        data = calculation_request_schema.load(request.get_json())
        result = subtract(data["a"], data["b"])
        return jsonify(result_response_schema.dump({"result": result}))

    @application.route("/multiply", methods=["POST"])
    def api_multiply():
        """Multiply two numbers."""
        data = calculation_request_schema.load(request.get_json())
        result = multiply(data["a"], data["b"])
        return jsonify(result_response_schema.dump({"result": result}))

    @application.route("/divide", methods=["POST"])
    def api_divide():
        """Divide a by b."""
        data = calculation_request_schema.load(request.get_json())
        try:
            result = divide(data["a"], data["b"])
        except ValueError as e:
            return jsonify({"detail": str(e)}), 400
        return jsonify(result_response_schema.dump({"result": result}))

    return application


# --- Module-level app for `flask run` and `python app.py` ---

app = create_app()


def main() -> None:
    """Run the server."""
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
