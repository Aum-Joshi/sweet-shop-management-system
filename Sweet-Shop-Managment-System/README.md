# Sweet Shop Management System

A comprehensive inventory management system built with Test-Driven Development (TDD) principles.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Open your browser:**
   ```
   http://localhost:5000
   ```

## Features

- Add, delete, and view sweet inventory
- Search by name, category, or price range
- Purchase sweets with stock validation
- Restock inventory items
- Real-time inventory analytics
- Clean, responsive web interface

## Testing

Run the comprehensive test suite:
```bash
pytest test_sweetshop.py -v
```

## Project Structure

```
sweet-shop-management-system/
├── sweetshop.py              # Core business logic
├── test_sweetshop.py         # Test suite (27 tests)
├── app.py                    # Flask web application
├── main.py                   # Application entry point
├── models.py                 # Data models
├── requirements.txt          # Dependencies
├── templates/
│   └── minimal_index.html    # Web interface
└── static/
    └── minimal_style.css     # Styling
```

## Technical Details

- **Python 3.11+** with Flask framework
- **pytest** for comprehensive testing (27 test cases)
- **TDD methodology** with Red-Green-Refactor cycle
- **SOLID principles** and clean code practices
- **Responsive design** with minimal, modern UI

Built with Test-Driven Development for technical assessment.