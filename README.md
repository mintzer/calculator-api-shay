# Calculator API

A simple calculator REST API built with Flask and Flask-SQLAlchemy.

## Setup

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

## Run

```bash
python app.py
```

The server runs on `http://localhost:8000` by default.

### Configuration

The following environment variables can be used to configure the application:

| Variable | Default | Description |
|----------|---------|-------------|
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///calculator.db` | Database connection URI |
| `SECRET_KEY` | `dev-secret-key` | Flask secret key |
| `FLASK_DEBUG` | `0` | Set to `1` to enable debug mode |
| `APP_HOST` | `0.0.0.0` | Host to bind the server to |
| `APP_PORT` | `8000` | Port to bind the server to |

## Endpoints

### Calculator Operations

All calculator endpoints accept POST requests with a JSON body `{"a": <number>, "b": <number>}` and return `{"result": <number>}`.

| Endpoint | Description |
|----------|-------------|
| `POST /add` | Add two numbers |
| `POST /subtract` | Subtract b from a |
| `POST /multiply` | Multiply two numbers |
| `POST /divide` | Divide a by b |

### Calculation History (CRUD)

Store calculations in a SQLite database.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/calculations` | Create & store a calculation |
| GET | `/calculations` | List all stored calculations |
| GET | `/calculations/<id>` | Get a specific calculation |
| DELETE | `/calculations/<id>` | Delete a calculation |

## Examples

**Quick calculation:**

```bash
curl -X POST http://localhost:8000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 5, "b": 3}'
```

Response: `{"result": 8.0}`

## Testing

Run the test suite with pytest:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```
