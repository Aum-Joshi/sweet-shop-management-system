"""
Entry point for the Sweet Shop Management System Flask application.

This module starts the Flask web server for the Sweet Shop Management System.
"""

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
