"""
Entrypoint for running the Flask application.
"""

from app import app

# PUBLIC_INTERFACE
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
