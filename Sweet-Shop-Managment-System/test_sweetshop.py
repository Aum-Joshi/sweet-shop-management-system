"""
Test suite for Sweet Shop Management System

This module contains comprehensive unit tests for the SweetShop class
following Test-Driven Development (TDD) principles.
"""

import pytest
from sweetshop import SweetShop, Sweet, InsufficientStockError, SweetNotFoundError


class TestSweetShop:
    """Test suite for SweetShop class."""
    
    def setup_method(self):
        """Set up a fresh SweetShop instance for each test."""
        self.shop = SweetShop()
    
    def test_shop_initialization(self):
        """Test that a new shop is initialized empty."""
        assert len(self.shop.sweets) == 0
        assert self.shop.get_all_sweets() == []
    
    def test_add_sweet_success(self):
        """Test successful addition of a sweet."""
        sweet_id = self.shop.add_sweet("Kaju Katli", "Nut-Based", 50.0, 20)
        
        assert sweet_id is not None
        assert len(self.shop.sweets) == 1
        
        sweet = self.shop.get_sweet_by_id(sweet_id)
        assert sweet['name'] == "Kaju Katli"
        assert sweet['category'] == "Nut-Based"
        assert sweet['price'] == 50.0
        assert sweet['quantity'] == 20
        assert sweet['id'] == sweet_id
    
    def test_add_sweet_with_invalid_name(self):
        """Test adding sweet with invalid name raises ValueError."""
        with pytest.raises(ValueError, match="Sweet name cannot be empty"):
            self.shop.add_sweet("", "Candy", 10.0, 5)
        
        with pytest.raises(ValueError, match="Sweet name cannot be empty"):
            self.shop.add_sweet("   ", "Candy", 10.0, 5)
    
    def test_add_sweet_with_invalid_category(self):
        """Test adding sweet with invalid category raises ValueError."""
        with pytest.raises(ValueError, match="Sweet category cannot be empty"):
            self.shop.add_sweet("Candy", "", 10.0, 5)
        
        with pytest.raises(ValueError, match="Sweet category cannot be empty"):
            self.shop.add_sweet("Candy", "   ", 10.0, 5)
    
    def test_add_sweet_with_invalid_price(self):
        """Test adding sweet with invalid price raises ValueError."""
        with pytest.raises(ValueError, match="Sweet price must be positive"):
            self.shop.add_sweet("Candy", "Sweet", 0.0, 5)
        
        with pytest.raises(ValueError, match="Sweet price must be positive"):
            self.shop.add_sweet("Candy", "Sweet", -10.0, 5)
    
    def test_add_sweet_with_invalid_quantity(self):
        """Test adding sweet with invalid quantity raises ValueError."""
        with pytest.raises(ValueError, match="Sweet quantity cannot be negative"):
            self.shop.add_sweet("Candy", "Sweet", 10.0, -5)
    
    def test_add_multiple_sweets(self):
        """Test adding multiple sweets."""
        id1 = self.shop.add_sweet("Kaju Katli", "Nut-Based", 50.0, 20)
        id2 = self.shop.add_sweet("Gajar Halwa", "Vegetable-Based", 30.0, 15)
        id3 = self.shop.add_sweet("Gulab Jamun", "Milk-Based", 10.0, 50)
        
        assert len(self.shop.sweets) == 3
        assert all(sweet_id in self.shop.sweets for sweet_id in [id1, id2, id3])
    
    def test_delete_sweet_success(self):
        """Test successful deletion of a sweet."""
        sweet_id = self.shop.add_sweet("Candy", "Sweet", 5.0, 10)
        assert len(self.shop.sweets) == 1
        
        result = self.shop.delete_sweet(sweet_id)
        assert result is True
        assert len(self.shop.sweets) == 0
        assert self.shop.get_sweet_by_id(sweet_id) is None
    
    def test_delete_sweet_not_found(self):
        """Test deletion of non-existent sweet."""
        result = self.shop.delete_sweet("nonexistent")
        assert result is False
        assert len(self.shop.sweets) == 0
    
    def test_get_all_sweets(self):
        """Test getting all sweets."""
        # Empty shop
        assert self.shop.get_all_sweets() == []
        
        # Add sweets
        self.shop.add_sweet("Sweet1", "Category1", 10.0, 5)
        self.shop.add_sweet("Sweet2", "Category2", 20.0, 15)
        
        all_sweets = self.shop.get_all_sweets()
        assert len(all_sweets) == 2
        assert all(isinstance(sweet, dict) for sweet in all_sweets)
        assert all('id' in sweet for sweet in all_sweets)
    
    def test_search_sweets_by_name(self):
        """Test searching sweets by name."""
        self.shop.add_sweet("Chocolate Cake", "Pastry", 100.0, 5)
        self.shop.add_sweet("Chocolate Bar", "Chocolate", 50.0, 20)
        self.shop.add_sweet("Vanilla Cake", "Pastry", 90.0, 8)
        
        # Test partial match
        results = self.shop.search_sweets_by_name("Chocolate")
        assert len(results) == 2
        
        # Test case insensitive
        results = self.shop.search_sweets_by_name("chocolate")
        assert len(results) == 2
        
        # Test exact match
        results = self.shop.search_sweets_by_name("Vanilla Cake")
        assert len(results) == 1
        assert results[0]['name'] == "Vanilla Cake"
        
        # Test no match
        results = self.shop.search_sweets_by_name("Nonexistent")
        assert len(results) == 0
        
        # Test empty search
        results = self.shop.search_sweets_by_name("")
        assert len(results) == 0
    
    def test_search_sweets_by_category(self):
        """Test searching sweets by category."""
        self.shop.add_sweet("Kaju Katli", "Nut-Based", 50.0, 20)
        self.shop.add_sweet("Almond Barfi", "Nut-Based", 60.0, 15)
        self.shop.add_sweet("Gulab Jamun", "Milk-Based", 10.0, 50)
        
        # Test exact match
        results = self.shop.search_sweets_by_category("Nut-Based")
        assert len(results) == 2
        
        # Test case insensitive
        results = self.shop.search_sweets_by_category("nut-based")
        assert len(results) == 2
        
        # Test single match
        results = self.shop.search_sweets_by_category("Milk-Based")
        assert len(results) == 1
        assert results[0]['name'] == "Gulab Jamun"
        
        # Test no match
        results = self.shop.search_sweets_by_category("Nonexistent")
        assert len(results) == 0
        
        # Test empty search
        results = self.shop.search_sweets_by_category("")
        assert len(results) == 0
    
    def test_search_sweets_by_price_range(self):
        """Test searching sweets by price range."""
        self.shop.add_sweet("Cheap Candy", "Candy", 5.0, 20)
        self.shop.add_sweet("Medium Sweet", "Sweet", 25.0, 15)
        self.shop.add_sweet("Expensive Chocolate", "Chocolate", 100.0, 5)
        
        # Test inclusive range
        results = self.shop.search_sweets_by_price_range(10.0, 50.0)
        assert len(results) == 1
        assert results[0]['name'] == "Medium Sweet"
        
        # Test edge cases
        results = self.shop.search_sweets_by_price_range(5.0, 5.0)
        assert len(results) == 1
        assert results[0]['name'] == "Cheap Candy"
        
        # Test wide range
        results = self.shop.search_sweets_by_price_range(0.0, 1000.0)
        assert len(results) == 3
        
        # Test no matches
        results = self.shop.search_sweets_by_price_range(200.0, 300.0)
        assert len(results) == 0
    
    def test_search_sweets_by_price_range_invalid_params(self):
        """Test price range search with invalid parameters."""
        with pytest.raises(ValueError, match="Prices cannot be negative"):
            self.shop.search_sweets_by_price_range(-10.0, 50.0)
        
        with pytest.raises(ValueError, match="Prices cannot be negative"):
            self.shop.search_sweets_by_price_range(10.0, -50.0)
        
        with pytest.raises(ValueError, match="Minimum price cannot be greater than maximum price"):
            self.shop.search_sweets_by_price_range(100.0, 50.0)
    
    def test_purchase_sweet_success(self):
        """Test successful sweet purchase."""
        sweet_id = self.shop.add_sweet("Candy", "Sweet", 10.0, 20)
        
        result = self.shop.purchase_sweet(sweet_id, 5)
        
        assert result['sweet_id'] == sweet_id
        assert result['sweet_name'] == "Candy"
        assert result['quantity_purchased'] == 5
        assert result['unit_price'] == 10.0
        assert result['total_cost'] == 50.0
        assert result['remaining_stock'] == 15
        
        # Verify stock was actually reduced
        sweet = self.shop.get_sweet_by_id(sweet_id)
        assert sweet['quantity'] == 15
    
    def test_purchase_sweet_insufficient_stock(self):
        """Test purchase with insufficient stock."""
        sweet_id = self.shop.add_sweet("Candy", "Sweet", 10.0, 5)
        
        with pytest.raises(InsufficientStockError, match="Insufficient stock. Available: 5, Requested: 10"):
            self.shop.purchase_sweet(sweet_id, 10)
        
        # Verify stock unchanged
        sweet = self.shop.get_sweet_by_id(sweet_id)
        assert sweet['quantity'] == 5
    
    def test_purchase_sweet_not_found(self):
        """Test purchase of non-existent sweet."""
        with pytest.raises(SweetNotFoundError, match="Sweet with ID 'nonexistent' not found"):
            self.shop.purchase_sweet("nonexistent", 1)
    
    def test_purchase_sweet_invalid_quantity(self):
        """Test purchase with invalid quantity."""
        sweet_id = self.shop.add_sweet("Candy", "Sweet", 10.0, 20)
        
        with pytest.raises(ValueError, match="Purchase quantity must be positive"):
            self.shop.purchase_sweet(sweet_id, 0)
        
        with pytest.raises(ValueError, match="Purchase quantity must be positive"):
            self.shop.purchase_sweet(sweet_id, -5)
    
    def test_restock_sweet_success(self):
        """Test successful sweet restocking."""
        sweet_id = self.shop.add_sweet("Candy", "Sweet", 10.0, 5)
        
        result = self.shop.restock_sweet(sweet_id, 15)
        
        assert result['sweet_id'] == sweet_id
        assert result['sweet_name'] == "Candy"
        assert result['quantity_added'] == 15
        assert result['previous_stock'] == 5
        assert result['new_stock'] == 20
        
        # Verify stock was actually increased
        sweet = self.shop.get_sweet_by_id(sweet_id)
        assert sweet['quantity'] == 20
    
    def test_restock_sweet_not_found(self):
        """Test restocking of non-existent sweet."""
        with pytest.raises(SweetNotFoundError, match="Sweet with ID 'nonexistent' not found"):
            self.shop.restock_sweet("nonexistent", 10)
    
    def test_restock_sweet_invalid_quantity(self):
        """Test restocking with invalid quantity."""
        sweet_id = self.shop.add_sweet("Candy", "Sweet", 10.0, 20)
        
        with pytest.raises(ValueError, match="Restock quantity must be positive"):
            self.shop.restock_sweet(sweet_id, 0)
        
        with pytest.raises(ValueError, match="Restock quantity must be positive"):
            self.shop.restock_sweet(sweet_id, -10)
    
    def test_get_low_stock_sweets(self):
        """Test getting low stock sweets."""
        self.shop.add_sweet("High Stock", "Sweet", 10.0, 100)
        self.shop.add_sweet("Medium Stock", "Sweet", 10.0, 10)
        self.shop.add_sweet("Low Stock", "Sweet", 10.0, 3)
        self.shop.add_sweet("Zero Stock", "Sweet", 10.0, 0)
        
        # Default threshold (5)
        low_stock = self.shop.get_low_stock_sweets()
        assert len(low_stock) == 2
        
        # Custom threshold
        low_stock = self.shop.get_low_stock_sweets(threshold=10)
        assert len(low_stock) == 3
        
        # High threshold
        low_stock = self.shop.get_low_stock_sweets(threshold=200)
        assert len(low_stock) == 4
    
    def test_get_total_inventory_value(self):
        """Test calculating total inventory value."""
        # Empty shop
        assert self.shop.get_total_inventory_value() == 0.0
        
        # Add sweets
        self.shop.add_sweet("Sweet1", "Category", 10.0, 5)  # Value: 50
        self.shop.add_sweet("Sweet2", "Category", 20.0, 3)  # Value: 60
        self.shop.add_sweet("Sweet3", "Category", 15.0, 0)  # Value: 0
        
        total_value = self.shop.get_total_inventory_value()
        assert total_value == 110.0


class TestSweet:
    """Test suite for Sweet class."""
    
    def test_sweet_creation(self):
        """Test sweet object creation."""
        sweet = Sweet("Test Sweet", "Test Category", 15.5, 10, "SW001")
        
        assert sweet.name == "Test Sweet"
        assert sweet.category == "Test Category"
        assert sweet.price == 15.5
        assert sweet.quantity == 10
        assert sweet.id == "SW001"
        assert isinstance(sweet.id, str)
        assert len(sweet.id) == 5  # SW001 format
    
    def test_sweet_to_dict(self):
        """Test sweet dictionary conversion."""
        sweet = Sweet("Test Sweet", "Test Category", 15.5, 10)
        sweet_dict = sweet.to_dict()
        
        expected_keys = {'id', 'name', 'category', 'price', 'quantity'}
        assert set(sweet_dict.keys()) == expected_keys
        assert sweet_dict['name'] == "Test Sweet"
        assert sweet_dict['category'] == "Test Category"
        assert sweet_dict['price'] == 15.5
        assert sweet_dict['quantity'] == 10
    
    def test_sweet_repr(self):
        """Test sweet string representation."""
        sweet = Sweet("Test Sweet", "Test Category", 15.5, 10)
        repr_str = repr(sweet)
        
        assert "Sweet(" in repr_str
        assert "Test Sweet" in repr_str
        assert "Test Category" in repr_str
        assert "15.5" in repr_str
        assert "10" in repr_str


# Integration tests
class TestSweetShopIntegration:
    """Integration tests for complete workflows."""
    
    def setup_method(self):
        """Set up shop with sample data."""
        self.shop = SweetShop()
        self.sample_data = [
            ("Kaju Katli", "Nut-Based", 50.0, 20),
            ("Gajar Halwa", "Vegetable-Based", 30.0, 15),
            ("Gulab Jamun", "Milk-Based", 10.0, 50),
            ("Chocolate Cake", "Pastry", 100.0, 5),
            ("Rasgulla", "Milk-Based", 8.0, 30)
        ]
        
        self.sweet_ids = []
        for name, category, price, quantity in self.sample_data:
            sweet_id = self.shop.add_sweet(name, category, price, quantity)
            self.sweet_ids.append(sweet_id)
    
    def test_complete_shop_workflow(self):
        """Test a complete shop management workflow."""
        # 1. Verify initial stock
        all_sweets = self.shop.get_all_sweets()
        assert len(all_sweets) == 5
        
        # 2. Search for milk-based sweets
        milk_sweets = self.shop.search_sweets_by_category("Milk-Based")
        assert len(milk_sweets) == 2
        
        # 3. Purchase some sweets
        gulab_jamun_id = None
        for sweet in all_sweets:
            if sweet['name'] == "Gulab Jamun":
                gulab_jamun_id = sweet['id']
                break
        
        purchase_result = self.shop.purchase_sweet(gulab_jamun_id, 20)
        assert purchase_result['total_cost'] == 200.0
        assert purchase_result['remaining_stock'] == 30
        
        # 4. Check low stock items
        low_stock = self.shop.get_low_stock_sweets()
        assert len(low_stock) == 1  # Only Chocolate Cake with 5 items
        
        # 5. Restock low stock item
        cake_id = low_stock[0]['id']
        restock_result = self.shop.restock_sweet(cake_id, 15)
        assert restock_result['new_stock'] == 20
        
        # 6. Verify no more low stock items
        low_stock_after = self.shop.get_low_stock_sweets()
        assert len(low_stock_after) == 0
        
        # 7. Calculate total inventory value
        total_value = self.shop.get_total_inventory_value()
        expected_value = (
            50 * 20 +      # Kaju Katli
            30 * 15 +      # Gajar Halwa  
            10 * 30 +      # Gulab Jamun (after purchase)
            100 * 20 +     # Chocolate Cake (after restock)
            8 * 30         # Rasgulla
        )
        assert total_value == expected_value
