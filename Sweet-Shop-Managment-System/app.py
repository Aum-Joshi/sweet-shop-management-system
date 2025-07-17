"""
Flask Web Application for Sweet Shop Management System

This module provides a web interface for the Sweet Shop Management System
using Flask framework with Bootstrap styling.
"""

import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from sweetshop import SweetShop, InsufficientStockError, SweetNotFoundError
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize Sweet Shop
shop = SweetShop()

# Add some sample data for demonstration
def initialize_sample_data():
    """Initialize the shop with sample data from the PDF."""
    sample_sweets = [
        ("Kaju Katli", "Nut-Based", 50.0, 20),
        ("Gajar Halwa", "Vegetable-Based", 30.0, 15),
        ("Gulab Jamun", "Milk-Based", 10.0, 50),
        ("Chocolate Cake", "Pastry", 100.0, 8),
        ("Rasgulla", "Milk-Based", 8.0, 30),
        ("Almond Barfi", "Nut-Based", 60.0, 12),
        ("Jalebi", "Syrup-Based", 15.0, 25)
    ]
    
    for name, category, price, quantity in sample_sweets:
        try:
            shop.add_sweet(name, category, price, quantity)
            app.logger.info(f"Added sample sweet: {name}")
        except Exception as e:
            app.logger.error(f"Error adding sample sweet {name}: {e}")

# Initialize sample data when app starts
initialize_sample_data()


@app.route('/')
def index():
    """Main dashboard page showing all sweets and statistics."""
    try:
        all_sweets = shop.get_all_sweets()
        low_stock_sweets = shop.get_low_stock_sweets()
        total_value = shop.get_total_inventory_value()
        
        # Get unique categories for filter dropdown
        categories = list(set(sweet['category'] for sweet in all_sweets))
        categories.sort()
        
        return render_template('minimal_index.html', 
                             sweets=all_sweets,
                             low_stock_count=len(low_stock_sweets),
                             total_value=total_value,
                             categories=categories)
    except Exception as e:
        app.logger.error(f"Error loading dashboard: {e}")
        flash(f"Error loading dashboard: {str(e)}", "error")
        return render_template('minimal_index.html', sweets=[], categories=[])


@app.route('/add_sweet', methods=['POST'])
def add_sweet():
    """Add a new sweet to the shop."""
    try:
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price = float(request.form.get('price', 0))
        quantity = int(request.form.get('quantity', 0))
        
        sweet_id = shop.add_sweet(name, category, price, quantity)
        flash(f"Sweet '{name}' added successfully! ID: {sweet_id}", "success")
        
    except ValueError as e:
        flash(f"Error adding sweet: {str(e)}", "error")
    except Exception as e:
        app.logger.error(f"Unexpected error adding sweet: {e}")
        flash("An unexpected error occurred while adding the sweet.", "error")
    
    return redirect(url_for('index'))


@app.route('/delete_sweet/<sweet_id>', methods=['POST'])
def delete_sweet(sweet_id):
    """Delete a sweet from the shop."""
    try:
        sweet = shop.get_sweet_by_id(sweet_id)
        if sweet:
            if shop.delete_sweet(sweet_id):
                flash(f"Sweet '{sweet['name']}' deleted successfully!", "success")
            else:
                flash("Error deleting sweet.", "error")
        else:
            flash("Sweet not found.", "error")
    except Exception as e:
        app.logger.error(f"Error deleting sweet {sweet_id}: {e}")
        flash("An error occurred while deleting the sweet.", "error")
    
    return redirect(url_for('index'))


@app.route('/search')
def search():
    """Search sweets by various criteria."""
    try:
        search_type = request.args.get('type', 'name')
        query = request.args.get('query', '').strip()
        
        results = []
        
        if query:
            if search_type == 'name':
                results = shop.search_sweets_by_name(query)
            elif search_type == 'category':
                results = shop.search_sweets_by_category(query)
            elif search_type == 'price_range':
                # Expect query in format "min-max"
                try:
                    min_price, max_price = map(float, query.split('-'))
                    results = shop.search_sweets_by_price_range(min_price, max_price)
                except ValueError:
                    flash("Invalid price range format. Use 'min-max' (e.g., '10-50')", "error")
                    return redirect(url_for('index'))
        
        return render_template('minimal_index.html', 
                             sweets=results,
                             search_query=query,
                             search_type=search_type,
                             categories=[])
                             
    except Exception as e:
        app.logger.error(f"Error searching sweets: {e}")
        flash(f"Error searching sweets: {str(e)}", "error")
        return redirect(url_for('index'))


@app.route('/purchase', methods=['POST'])
def purchase_sweet():
    """Purchase sweets (decrease stock)."""
    try:
        sweet_id = request.form.get('sweet_id')
        quantity = int(request.form.get('quantity', 0))
        
        result = shop.purchase_sweet(sweet_id, quantity)
        
        flash(f"Purchased {result['quantity_purchased']} x {result['sweet_name']} "
              f"for ₹{result['total_cost']:.2f}. Remaining stock: {result['remaining_stock']}", 
              "success")
              
    except InsufficientStockError as e:
        flash(str(e), "error")
    except SweetNotFoundError as e:
        flash(str(e), "error")
    except ValueError as e:
        flash(f"Invalid purchase quantity: {str(e)}", "error")
    except Exception as e:
        app.logger.error(f"Error purchasing sweet: {e}")
        flash("An error occurred while processing the purchase.", "error")
    
    return redirect(url_for('index'))


@app.route('/restock', methods=['POST'])
def restock_sweet():
    """Restock sweets (increase stock)."""
    try:
        sweet_id = request.form.get('sweet_id')
        quantity = int(request.form.get('quantity', 0))
        
        result = shop.restock_sweet(sweet_id, quantity)
        
        flash(f"Restocked {result['quantity_added']} x {result['sweet_name']}. "
              f"New stock: {result['new_stock']}", "success")
              
    except SweetNotFoundError as e:
        flash(str(e), "error")
    except ValueError as e:
        flash(f"Invalid restock quantity: {str(e)}", "error")
    except Exception as e:
        app.logger.error(f"Error restocking sweet: {e}")
        flash("An error occurred while restocking the sweet.", "error")
    
    return redirect(url_for('index'))



@app.route('/api/sweets')
def api_get_sweets():
    """API endpoint to get all sweets in JSON format."""
    try:
        sweets = shop.get_all_sweets()
        return jsonify({
            'success': True,
            'sweets': sweets,
            'count': len(sweets)
        })
    except Exception as e:
        app.logger.error(f"API error getting sweets: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sweet/<sweet_id>')
def api_get_sweet(sweet_id):
    """API endpoint to get a specific sweet by ID."""
    try:
        sweet = shop.get_sweet_by_id(sweet_id)
        if sweet:
            return jsonify({
                'success': True,
                'sweet': sweet
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Sweet not found'
            }), 404
    except Exception as e:
        app.logger.error(f"API error getting sweet {sweet_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats')
def api_get_stats():
    """API endpoint to get shop statistics."""
    try:
        all_sweets = shop.get_all_sweets()
        low_stock_sweets = shop.get_low_stock_sweets()
        total_value = shop.get_total_inventory_value()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_sweets': len(all_sweets),
                'low_stock_count': len(low_stock_sweets),
                'total_inventory_value': total_value,
                'categories': list(set(sweet['category'] for sweet in all_sweets))
            }
        })
    except Exception as e:
        app.logger.error(f"API error getting stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('minimal_index.html', 
                         sweets=[], 
                         categories=[],
                         error_message="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    app.logger.error(f"Internal server error: {error}")
    return render_template('minimal_index.html', 
                         sweets=[], 
                         categories=[],
                         error_message="Internal server error"), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
