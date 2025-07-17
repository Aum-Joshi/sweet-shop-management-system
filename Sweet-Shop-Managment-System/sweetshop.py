"""
Sweet Shop Management System Core Module

This module contains the main SweetShop class that handles all
sweet management operations including adding, deleting, searching,
purchasing, and restocking sweets.
"""

from typing import List, Dict, Optional, Tuple


class Sweet:
    """Represents a sweet item in the shop."""
    
    def __init__(self, name: str, category: str, price: float, quantity: int, sweet_id: str = None):
        """
        Initialize a sweet with basic properties.
        
        Args:
            name (str): Name of the sweet
            category (str): Category (e.g., chocolate, candy, pastry)
            price (float): Price per unit
            quantity (int): Quantity in stock
            sweet_id (str): Optional custom ID for the sweet
        """
        self.id = sweet_id  # Will be set by SweetShop
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
    
    def to_dict(self) -> Dict:
        """Convert sweet to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity
        }
    
    def __repr__(self) -> str:
        return f"Sweet(id='{self.id}', name='{self.name}', category='{self.category}', price={self.price}, quantity={self.quantity})"


class InsufficientStockError(Exception):
    """Raised when there's not enough stock for a purchase."""
    pass


class SweetNotFoundError(Exception):
    """Raised when a sweet with given ID is not found."""
    pass


class SweetShop:
    """Main class for managing the sweet shop operations."""
    
    def __init__(self):
        """Initialize empty sweet shop."""
        self.sweets: Dict[str, Sweet] = {}
        self._next_id = 1  # Counter for generating sequential IDs
    
    def add_sweet(self, name: str, category: str, price: float, quantity: int) -> str:
        """
        Add a new sweet to the shop.
        
        Args:
            name (str): Name of the sweet
            category (str): Category of the sweet
            price (float): Price per unit
            quantity (int): Initial quantity
            
        Returns:
            str: ID of the newly added sweet
            
        Raises:
            ValueError: If any parameter is invalid
        """
        if not name or not name.strip():
            raise ValueError("Sweet name cannot be empty")
        if not category or not category.strip():
            raise ValueError("Sweet category cannot be empty")
        if price <= 0:
            raise ValueError("Sweet price must be positive")
        if quantity < 0:
            raise ValueError("Sweet quantity cannot be negative")
        
        # Generate clean sequential ID
        sweet_id = f"SW{self._next_id:03d}"  # SW001, SW002, etc.
        self._next_id += 1
        
        sweet = Sweet(name.strip(), category.strip(), price, quantity, sweet_id)
        self.sweets[sweet.id] = sweet
        return sweet.id
    
    def delete_sweet(self, sweet_id: str) -> bool:
        """
        Delete a sweet from the shop.
        
        Args:
            sweet_id (str): ID of the sweet to delete
            
        Returns:
            bool: True if sweet was deleted, False if not found
        """
        if sweet_id in self.sweets:
            del self.sweets[sweet_id]
            return True
        return False
    
    def get_all_sweets(self) -> List[Dict]:
        """
        Get all sweets in the shop.
        
        Returns:
            List[Dict]: List of all sweets as dictionaries
        """
        return [sweet.to_dict() for sweet in self.sweets.values()]
    
    def get_sweet_by_id(self, sweet_id: str) -> Optional[Dict]:
        """
        Get a sweet by its ID.
        
        Args:
            sweet_id (str): ID of the sweet
            
        Returns:
            Optional[Dict]: Sweet data if found, None otherwise
        """
        sweet = self.sweets.get(sweet_id)
        return sweet.to_dict() if sweet else None
    
    def search_sweets_by_name(self, name: str) -> List[Dict]:
        """
        Search sweets by name (case-insensitive partial match).
        
        Args:
            name (str): Name to search for
            
        Returns:
            List[Dict]: List of matching sweets
        """
        if not name:
            return []
        
        name_lower = name.lower()
        return [
            sweet.to_dict() 
            for sweet in self.sweets.values() 
            if name_lower in sweet.name.lower()
        ]
    
    def search_sweets_by_category(self, category: str) -> List[Dict]:
        """
        Search sweets by category (case-insensitive exact match).
        
        Args:
            category (str): Category to search for
            
        Returns:
            List[Dict]: List of matching sweets
        """
        if not category:
            return []
        
        category_lower = category.lower()
        return [
            sweet.to_dict() 
            for sweet in self.sweets.values() 
            if sweet.category.lower() == category_lower
        ]
    
    def search_sweets_by_price_range(self, min_price: float, max_price: float) -> List[Dict]:
        """
        Search sweets by price range (inclusive).
        
        Args:
            min_price (float): Minimum price
            max_price (float): Maximum price
            
        Returns:
            List[Dict]: List of matching sweets
            
        Raises:
            ValueError: If min_price > max_price or negative prices
        """
        if min_price < 0 or max_price < 0:
            raise ValueError("Prices cannot be negative")
        if min_price > max_price:
            raise ValueError("Minimum price cannot be greater than maximum price")
        
        return [
            sweet.to_dict() 
            for sweet in self.sweets.values() 
            if min_price <= sweet.price <= max_price
        ]
    
    def purchase_sweet(self, sweet_id: str, quantity: int) -> Dict:
        """
        Purchase sweets, decreasing the stock.
        
        Args:
            sweet_id (str): ID of the sweet to purchase
            quantity (int): Quantity to purchase
            
        Returns:
            Dict: Purchase details including total cost
            
        Raises:
            SweetNotFoundError: If sweet ID is not found
            InsufficientStockError: If not enough stock available
            ValueError: If quantity is invalid
        """
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        
        if sweet_id not in self.sweets:
            raise SweetNotFoundError(f"Sweet with ID '{sweet_id}' not found")
        
        sweet = self.sweets[sweet_id]
        
        if sweet.quantity < quantity:
            raise InsufficientStockError(
                f"Insufficient stock. Available: {sweet.quantity}, Requested: {quantity}"
            )
        
        sweet.quantity -= quantity
        total_cost = sweet.price * quantity
        
        return {
            'sweet_id': sweet_id,
            'sweet_name': sweet.name,
            'quantity_purchased': quantity,
            'unit_price': sweet.price,
            'total_cost': total_cost,
            'remaining_stock': sweet.quantity
        }
    
    def restock_sweet(self, sweet_id: str, quantity: int) -> Dict:
        """
        Restock sweets, increasing the stock.
        
        Args:
            sweet_id (str): ID of the sweet to restock
            quantity (int): Quantity to add to stock
            
        Returns:
            Dict: Restock details
            
        Raises:
            SweetNotFoundError: If sweet ID is not found
            ValueError: If quantity is invalid
        """
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive")
        
        if sweet_id not in self.sweets:
            raise SweetNotFoundError(f"Sweet with ID '{sweet_id}' not found")
        
        sweet = self.sweets[sweet_id]
        old_quantity = sweet.quantity
        sweet.quantity += quantity
        
        return {
            'sweet_id': sweet_id,
            'sweet_name': sweet.name,
            'quantity_added': quantity,
            'previous_stock': old_quantity,
            'new_stock': sweet.quantity
        }
    
    def get_low_stock_sweets(self, threshold: int = 5) -> List[Dict]:
        """
        Get sweets with stock below the threshold.
        
        Args:
            threshold (int): Stock threshold (default: 5)
            
        Returns:
            List[Dict]: List of low stock sweets
        """
        return [
            sweet.to_dict() 
            for sweet in self.sweets.values() 
            if sweet.quantity <= threshold
        ]
    
    def get_total_inventory_value(self) -> float:
        """
        Calculate total value of all inventory.
        
        Returns:
            float: Total inventory value
        """
        return sum(sweet.price * sweet.quantity for sweet in self.sweets.values())
