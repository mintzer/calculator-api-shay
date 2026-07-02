#!/usr/bin/env python3
"""Flask calculator REST API server."""

from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from core import add, divide, multiply, subtract

db = SQLAlchemy()

OPERATIONS = {
    "add": add,
    "sub": subtract,
    "mul": multiply,
    "div": divide,
}


class Calculation(db.Model):
    """Database model for stored calculations."""

    __tablename__ = "calculation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operation = db.Column(db.String, nullable=False)
    a = db.Column(db.Float, nullable=False)
    b = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


def calculation_to_dict(c: Calculation) -> dict:
    """Convert a Calculation model instance to a JSON-serialisable dict."""
    return {
        "id": c.id,
        "operation": c.operation,
        "a": c.a,
        "b": c.b,
        "result": c.result,
        "created_at": c.created_at.isoformat(),
    }


def create_app(config: dict | None = None) -> Flask:
    """Application factory."""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calculator.db"
    if config:
        app.config.update(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ------------------------------------------------------------------
    # Error handlers
    # ------------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(exc):
        return jsonify({"detail": str(exc) or "Bad request"}), 400

    @app.errorhandler(KeyError)
    def missing_field(exc):
        return jsonify({"detail": f"Missing required field: {exc}"}), 400

    @app.errorhandler(TypeError)
    def invalid_field(exc):
        return jsonify({"detail": f"Invalid field value: {exc}"}), 400

    @app.errorhandler(404)
    def not_found(exc):
        return jsonify({"detail": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(exc):
        return jsonify({"detail": "Method not allowed"}), 405

    # ------------------------------------------------------------------
    # Calculator endpoints
    # ------------------------------------------------------------------

    @app.post("/add")
    def api_add():
        """Add two numbers."""
        data = request.get_json(force=True)
        return jsonify({"result": add(data["a"], data["b"])}), 200

    @app.post("/subtract")
    def api_subtract():
        """Subtract b from a."""
        data = request.get_json(force=True)
        return jsonify({"result": subtract(data["a"], data["b"])}), 200

    @app.post("/multiply")
    def api_multiply():
        """Multiply two numbers."""
        data = request.get_json(force=True)
        return jsonify({"result": multiply(data["a"], data["b"])}), 200

    @app.post("/divide")
    def api_divide():
        """Divide a by b."""
        data = request.get_json(force=True)
        try:
            return jsonify({"result": divide(data["a"], data["b"])}), 200
        except ValueError as exc:
            return jsonify({"detail": str(exc)}), 400

    # ------------------------------------------------------------------
    # CRUD endpoints for Calculations
    # ------------------------------------------------------------------

    @app.post("/calculations")
    def create_calculation():
        """Create and store a new calculation."""
        data = request.get_json(force=True)
        if data is None:
            return jsonify({"detail": "Request body must be valid JSON"}), 400
        operation = data.get("operation")
        if operation not in OPERATIONS:
            return (
                jsonify(
                    {
                        "detail": (
                            f"Unknown operation: {operation}. Use: {list(OPERATIONS)}"
                        )
                    }
                ),
                400,
            )
        try:
            result = OPERATIONS[operation](data["a"], data["b"])
        except ValueError as exc:
            return jsonify({"detail": str(exc)}), 400

        calc = Calculation(
            operation=operation,
            a=data["a"],
            b=data["b"],
            result=result,
        )
        db.session.add(calc)
        db.session.commit()
        return jsonify(calculation_to_dict(calc)), 201

    @app.get("/calculations")
    def list_calculations():
        """List all stored calculations, newest first."""
        calcs = Calculation.query.order_by(Calculation.created_at.desc()).all()
        return jsonify([calculation_to_dict(c) for c in calcs]), 200

    @app.get("/calculations/<int:calculation_id>")
    def get_calculation(calculation_id: int):
        """Get a specific calculation by ID."""
        calc = db.session.get(Calculation, calculation_id)
        if calc is None:
            return jsonify({"detail": "Calculation not found"}), 404
        return jsonify(calculation_to_dict(calc)), 200

    @app.delete("/calculations/<int:calculation_id>")
    def delete_calculation(calculation_id: int):
        """Delete a calculation by ID."""
        calc = db.session.get(Calculation, calculation_id)
        if calc is None:
            return jsonify({"detail": "Calculation not found"}), 404
        db.session.delete(calc)
        db.session.commit()
        return "", 204

    return app


def main() -> None:
    """Run the development server."""
    app = create_app()
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
